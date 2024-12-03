import subprocess
import threading


def get_homebrew_cask_names():
    try:
        result = subprocess.run(
            ["brew", "list", "--cask"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if result.stderr:
            print("Error:", result.stderr)
            return []
        return result.stdout.splitlines()
    except Exception as e:
        print("An error occurred:", e)
        return []


def upgrade_cask(cask_name, results):
    # Run the command and capture its output
    result = subprocess.run(
        ["brew", "upgrade", "--cask", cask_name],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    results[cask_name] = result.stdout if result.stdout else result.stderr


def main():
    cask_names = get_homebrew_cask_names()
    results = subprocess.run(["brew", "update"])

    threads = []
    results = {}

    # Use multi-threading to update all casks
    for cask_name in cask_names:
        thread = threading.Thread(target=upgrade_cask, args=(cask_name, results))
        thread.start()
        threads.append(thread)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    # alphabetically sort the results based on cask name
    results = dict(sorted(results.items()))

    # Print out all casks that were actually updated
    print("\nUpdated casks:")
    for cask_name, output in results.items():
        if "Warning:" not in output:
            print(cask_name)

    # Print out all casks that were not updated
    print("\nNot updated casks:")
    for cask_name, output in results.items():
        if "Warning: Not upgrading" in output:
            print(cask_name)

    # Check for wrong cask names
    printed_error = False
    for cask_name, output in results.items():
        if "formula" in output:
            if not printed_error:
                printed_error = True
                print("\nFormula error (name error):")
            print(cask_name)

    if not printed_error:
        print("\nNo formula errors found")


if __name__ == "__main__":
    main()
