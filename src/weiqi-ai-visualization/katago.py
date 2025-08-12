from datetime import datetime
import subprocess
import json
import os


class KataGo:
    """A class to manage the KataGo AI engine for Weiqi games."""

    log_dir = "src/katago/logs/"
    os.makedirs(log_dir, exist_ok=True)
    log_filename = f"katago_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
    log_file = open(os.path.join(log_dir, log_filename), "w")

    def __init__(self):
        """Initialize the KataGo instance."""
        self.process = None

    def start(self):
        """Start the KataGo process with the specified model and configuration."""
        self.process = subprocess.Popen(
            [
                "katago",
                "analysis",
                "-model",
                "src/katago/models/kata1-b18c384nbt.bin.gz",
                "-config",
                "src/katago/configs/analysis_example.cfg",
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=self.log_file,
            text=True,
        )

    def send_request(self, request: dict):
        """Send a request to the KataGo process.

        Args:
            request (dict): The request to send to the KataGo process.

        Raises:
            RuntimeError: If the KataGo process is not running.

        Returns:
            dict: The response from the KataGo process.
        """
        if self.process is None:
            raise RuntimeError("KataGo process is not running.")

        self.process.stdin.write(json.dumps(request) + "\n")
        self.process.stdin.flush()

        response_line = self.process.stdout.readline()
        response = json.loads(response_line)
        return response

    def stop(self):
        """Stop the KataGo process and close the log file.

        Raises:
            RuntimeError: If the KataGo process is not running.
        """
        if self.process is None:
            raise RuntimeError("KataGo process is not running.")

        self.process.stdin.write("exit\n")
        self.process.stdin.flush()
        self.process.wait()
        self.process = None
        self.log_file.close()
        self.log_file = None

    @property
    def is_running(self):
        """Check if the KataGo process is currently running."""
        return self.process is not None and self.process.poll() is None
