import asyncio
import datetime
from pathlib import Path
from scrapli import AsyncScrapli

# Function to fetch data from the Arista switches
async def fetch_data(ip, username, password):
    # Device configuration dictionary
    device = {
        'host': ip,
        'auth_username': username,
        'auth_password': password,
        'auth_strict_key': False,
        'transport': 'asyncssh',
        'platform': 'arista_eos',
    }

    # List of commands to execute on the switch
    commands = [
        'show lldp neighbors',
        'show ip route',
        'show ip bgp summary',
        'show ip bgp neighbors',
        'show version',
    ]

    # Async context manager to establish connection with the switch
    async with AsyncScrapli(**device) as connection:
        # Create backup directory for the switch
        backup_dir = Path(f'/home/backups/arista/{ip}/')
        backup_dir.mkdir(parents=True, exist_ok=True)

        # Get the current date and time
        current_datetime = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

        # Iterate through the commands
        for command in commands:
            # Execute the command and get the output
            output = await connection.send_command(command)
            print(output.result)

            # Create a file name with the current date and time, network state, and command
            file_name = f"{current_datetime}_networkstate_{command.replace(' ', '_')}.txt"
            file_path = backup_dir / file_name

            # Write the output to the file
            with file_path.open('w') as f:
                f.write(output.result)

            # Print the file path where the output was saved
            print(f"Saved {command} output to: {file_path}")

# Main async function to run the tasks
async def main():
    # List of switch IP addresses
    ips = [
        'leaf1',
        'leaf2',
    ]

    # Switch credentials
    username = 'admin'
    password = 'arista'

    # Create a list of tasks for each switch
    tasks = [fetch_data(ip, username, password) for ip in ips]
    # Run the tasks concurrently
    await asyncio.gather(*tasks)

# Entry point of the script
if __name__ == "__main__":
    # Run the main async function
    asyncio.run(main())
