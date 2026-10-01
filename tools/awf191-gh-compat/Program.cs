using System.Diagnostics;
using System.Security.Cryptography;
using System.Text.RegularExpressions;

internal static class Program
{
    // SHA-256 of the verified GitHub CLI 2.102.0 gh.exe used for this observation.
    private const string GhSha256 = "756724853cc579510b58e65e7a7429ad6b1af29cf99ef19b3a95f3b701c5c580";
    private static readonly Regex Pr = new(@"^repos/jkinlay/cooling-fluid/pulls/[1-9][0-9]*$", RegexOptions.CultureInvariant);
    private static readonly Regex PrFiles = new(@"^repos/jkinlay/cooling-fluid/pulls/[1-9][0-9]*/files\?per_page=100&page=[1-5]$", RegexOptions.CultureInvariant);
    private static readonly Regex AllowedEndpoint = new(
        @"^repos/jkinlay/cooling-fluid(?:$|/branches/main$|/commits/[0-9a-f]{40}/pulls\?per_page=100$|/pulls/[1-9][0-9]*(?:/files\?per_page=100&page=[1-5])?$|/contents/\.agentic/installed-manifest\.json\?ref=[0-9a-f]{40}$|/git/commits/[0-9a-f]{40}$|/git/trees/[0-9a-f]{40}(?:\?recursive=1)?$)",
        RegexOptions.CultureInvariant);

    private static async Task<byte[]> ReadBoundedAsync(Stream source, int limit, CancellationToken cancellation)
    {
        using var output = new MemoryStream();
        var buffer = new byte[8192];
        while (true)
        {
            var count = await source.ReadAsync(buffer, cancellation);
            if (count == 0) return output.ToArray();
            if (output.Length + count > limit) throw new InvalidDataException("GitHub response exceeds bound");
            output.Write(buffer, 0, count);
        }
    }

    private static async Task<int> Main(string[] args)
    {
        // Accept only the exact, read-only call shape emitted by AWF 1.9.1.
        if (args.Length != 10 || args[0] != "api" || args[1] != "--hostname" || args[2] != "github.com" ||
            args[3] != "--method" || args[4] != "GET" || args[5] != "-H" ||
            args[6] != "Accept: application/vnd.github+json" || args[7] != "-H" ||
            args[8] != "X-GitHub-Api-Version: 2026-03-10" || !AllowedEndpoint.IsMatch(args[9]))
        {
            Console.Error.WriteLine("Unsupported AWF GitHub request");
            return 2;
        }

        var gh = Environment.GetEnvironmentVariable("AWF191_GH_EXE");
        if (string.IsNullOrWhiteSpace(gh) || !Path.IsPathFullyQualified(gh) || !File.Exists(gh))
        {
            Console.Error.WriteLine("Pinned GitHub CLI is unavailable");
            return 2;
        }
        try
        {
            await using var stream = File.OpenRead(gh);
            var digest = Convert.ToHexString(await SHA256.HashDataAsync(stream));
            if (!digest.Equals(GhSha256, StringComparison.OrdinalIgnoreCase))
            {
                Console.Error.WriteLine("GitHub CLI digest mismatch");
                return 2;
            }

            var endpoint = args[9];
            var info = new ProcessStartInfo(gh)
            {
                UseShellExecute = false,
                CreateNoWindow = true,
                RedirectStandardOutput = true,
                RedirectStandardError = true
            };
            foreach (var arg in args)
            {
                info.ArgumentList.Add(arg == "X-GitHub-Api-Version: 2026-03-10" && Pr.IsMatch(endpoint)
                    ? "X-GitHub-Api-Version: 2022-11-28" : arg);
            }
            if (PrFiles.IsMatch(endpoint))
            {
                // Preserve every entry's identity, status, and blob SHA, omitting patch bodies.
                info.ArgumentList.Add("--jq");
                info.ArgumentList.Add("map({filename,status,sha})");
            }
            using var process = Process.Start(info);
            if (process is null)
            {
                Console.Error.WriteLine("GitHub CLI did not start");
                return 3;
            }
            using var timeout = new CancellationTokenSource(TimeSpan.FromSeconds(20));
            var output = ReadBoundedAsync(process.StandardOutput.BaseStream, 1024 * 1024, timeout.Token);
            var error = ReadBoundedAsync(process.StandardError.BaseStream, 4096, timeout.Token);
            try
            {
                await Task.WhenAll(output, error, process.WaitForExitAsync(timeout.Token));
            }
            catch (Exception)
            {
                if (!process.HasExited) process.Kill(entireProcessTree: true);
                Console.Error.WriteLine("GitHub GET exceeded its bound or failed");
                return 3;
            }
            if (process.ExitCode != 0)
            {
                Console.Error.WriteLine("GitHub GET failed");
                return 3;
            }
            await Console.OpenStandardOutput().WriteAsync(await output);
            return 0;
        }
        catch (Exception)
        {
            Console.Error.WriteLine("GitHub observation failed");
            return 3;
        }
    }
}