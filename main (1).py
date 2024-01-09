import socket
import ssl
from datetime import datetime
import pickle
import psutil
import subprocess
import platform
from em import email_alert


class Server:
    def __init__(self, name, port, connection, priority):
        self.name = name
        self.port = port
        self.connection = connection.lower()
        self.priority = priority.lower()

        self.history = []
        self.alert = False

    def check_connection(self):
        msg = "The Server is down!"
        success = False
        now = datetime.now()

        try:
            if self.connection == "plain":
                socket.create_connection((self.name, self.port), timeout=10)
                msg = f"{self.name} is up. On port {self.port} with {self.connection}"
                success = True
                self.alert = True

            elif self.connection == "ssl":
                ssl.wrap_socket(socket.create_connection((self.name, self.port), timeout=10))
                msg = f"{self.name} is up. On port {self.port} with {self.connection}"
                success = True
                self.alert = False
            else:
                if self.ping():
                    msg = f"{self.name} is up. On port {self.port} with {self.connection}"
                    success = True
                    self.alert = False

        except socket.timeout:
            msg = f"server: {self.name} timeout. on port {self.port}"
        except (ConnectionRefusedError, ConnectionResetError) as e:
            msg = f"server: {self.name} {e}"
        except Exception as e:
            msg = f"No Idea?: {e}"

        if success == False and self.alert == False:
            self.alert = True
            email_alert(self.name, f"{msg}\n{now}", "bajotatu@altmails.com")

        self.create_history(msg, success, now)

    def create_history(self, msg, success, now):
        history_max = 100
        self.history.append((msg, success, now))

        while len(self.history) > history_max:
            self.history.pop(0)

    def ping(self):
        try:
            output = subprocess.check_output("ping -{} 1 {}".format('n' if platform.system().lower(
            ) == "windows" else 'c', self.name), shell=True, universal_newlines=True)
            if 'unreachable' in output:
                return False
            else:
                return True
        except Exception:
            return False


if __name__ == "__main__":
    try:
        servers = pickle.load(open("servers.pick", "rb"))
    except:
        servers = [
            Server("apache.com", 80, "plain", "high"),
            Server("msn.com", 80, "plain", "high"),
            Server("smtp.gmail.com", 587, "ssl", "high"),
            Server("192.168.207.20", 80, "ping", "high")
        ]

    for server in servers:
        server.check_connection()
        print(server.history[-1])
        print(len(server.history))

    mem_usage = psutil.virtual_memory()

    print(f"Free: {mem_usage.percent}%")
    print(f"Total: {mem_usage.total / (1024 ** 3):.2f}G")
    print(f"Used: {mem_usage.used / (1024 ** 3):.2f}G")

    per_cpu = psutil.cpu_percent(percpu=True, interval=1)
    for idx, usage in enumerate(per_cpu):
        print(f"CORE_{idx + 1}: {usage}%")

    pickle.dump(servers, open("servers.pickle", "wb"))
