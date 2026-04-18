import subprocess
import sys

def main():
    print("🚀 Starting Hugo Build...")
    try:
        # Construct the command
        command = ["npx", "--yes", "hugo-bin", "--gc", "--minify", "--destination", "static"]

        # Execute the command
        result = subprocess.run(command, shell=True, check=True)

        if result.returncode == 0:
            print("\n✅ Build complete! Site generated in 'static/' directory.")
        else:
            print(f"\n❌ Build failed with return code: {result.returncode}")
            sys.exit(result.returncode)

    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error during build: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
