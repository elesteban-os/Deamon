
import os
import sys
import time
import signal
import logging
from logging.handlers import RotatingFileHandler
import subprocess
import re

script_dir = os.path.dirname(os.path.abspath(__file__))
icon_path = os.path.join(script_dir, "of.png")

def get_cpu_temperature():
        try:
            output = subprocess.check_output("sensors", text=True)
            match = re.search(r'k10temp.*?\n.*?Tctl:\s+\+([0-9.]+)°C', output, re.DOTALL)
            if match:
                return float(match.group(1))
        except Exception as e:
            print(f"Error obteniendo temperatura: {e}")
        return 0.0


class TemperatureDaemon:
    def __init__(self, pidfile, logfile, threshold=65, interval=5):
        self.pidfile = pidfile
        self.logfile = logfile
        self.threshold = threshold
        self.interval = interval
        self.running = False
        
        # Configurar logging
        self.logger = logging.getLogger('TemperatureDaemon')
        self.logger.setLevel(logging.INFO)
        handler = RotatingFileHandler(
            logfile, maxBytes=1024*1024, backupCount=5
        )
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        
    def daemonize(self):
        """Double fork magic to create a daemon"""
        try:
            pid = os.fork()
            if pid > 0:
                # Exit first parent
                sys.exit(0)
        except OSError as err:
            self.logger.error(f'First fork failed: {err}')
            sys.exit(1)
        
        # Decouple from parent environment
        os.chdir('/')
        os.setsid()
        os.umask(0)
        
        # Do second fork
        try:
            pid = os.fork()
            if pid > 0:
                # Exit from second parent
                sys.exit(0)
        except OSError as err:
            self.logger.error(f'Second fork failed: {err}')
            sys.exit(1)
        
        # Redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        si = open(os.devnull, 'r')
        so = open(os.devnull, 'a+')
        se = open(os.devnull, 'a+')
        
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())
        
        # Write pidfile
        with open(self.pidfile, 'w') as f:
            f.write(str(os.getpid()))
        
        # Set signal handlers
        signal.signal(signal.SIGTERM, self.handle_signal)
        signal.signal(signal.SIGINT, self.handle_signal)
    
    def handle_signal(self, signum, frame):
        """Handle signals like SIGTERM and SIGINT"""
        self.logger.info(f'Received signal {signum}, shutting down...')
        self.running = False
    
    def run(self):
        """Main daemon loop"""
        self.running = True
        self.logger.info("Daemon started")
        
        while self.running:
            temp = get_cpu_temperature()
            self.logger.info(f"CPU Temperature: {temp}°C")
            
            if temp > self.threshold:
                self.logger.warning(f"Temperature threshold exceeded: {temp}°C > {self.threshold}°C")
                try:
                    #notification.notify("Only-Fans Daemon", "El daemon para los ventiladores se encuentra en ejecución.", app_icon=icon_path)
                    play_beep()
                    print("se ha exedido el umbral de temperatura")
                except Exception as e:
                    self.logger.error(f"Failed to send notification: {e}")
            
            time.sleep(self.interval)
        
        self.logger.info("Daemon stopped")
        os.remove(self.pidfile)
    
    def start(self):
        """Start the daemon"""
        # Check if pidfile exists
        if os.path.exists(self.pidfile):
            with open(self.pidfile, 'r') as f:
                pid = int(f.read())
            
            # Check if process is still running
            try:
                os.kill(pid, 0)
                print(f"Daemon already running with PID {pid}")
                sys.exit(1)
            except OSError:
                # Process not running, remove stale pidfile
                os.remove(self.pidfile)
        
        # Start the daemon
        self.daemonize()
        self.run()
    
    def stop(self):
        """Stop the daemon"""
        if not os.path.exists(self.pidfile):
            print("Daemon not running")
            return
        
        with open(self.pidfile, 'r') as f:
            pid = int(f.read())
        
        try:
            os.kill(pid, signal.SIGTERM)
        except OSError as err:
            print(f"Error stopping daemon: {err}")
            if os.path.exists(self.pidfile):
                os.remove(self.pidfile)
    
    def restart(self):
        """Restart the daemon"""
        self.stop()
        time.sleep(1)
        self.start()

def play_beep():
    beep_path = os.path.join(script_dir, "beep.wav")
    os.system(f'aplay {beep_path}')


if __name__ == '__main__':
    
    play_beep()
    # notification.notify("Only-Fans Daemon", "El daemon para los ventiladores se encuentra en ejecución.", app_icon=icon_path)    # Configuración (puedes modificar estos valores)
    PID_FILE = '/var/run/temperature_daemon.pid'
    LOG_FILE = '/var/log/temperature_daemon.log'
    THRESHOLD = 65  # °C
    INTERVAL = 5    # segundos
    
    daemon = TemperatureDaemon(PID_FILE, LOG_FILE, THRESHOLD, INTERVAL)
    
    if len(sys.argv) == 2:
        if sys.argv[1] == 'start':
            daemon.start()
        elif sys.argv[1] == 'stop':
            daemon.stop()
        elif sys.argv[1] == 'restart':
            daemon.restart()
        else:
            print("Usage: temperature_daemon.py start|stop|restart")
            sys.exit(2)
        sys.exit(0)
    else:
        print("Usage: temperature_daemon.py start|stop|restart")