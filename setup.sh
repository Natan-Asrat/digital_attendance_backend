#!/bin/bash

# Define the project directory
PROJECT_DIR="$(pwd)"

# Create the run.sh script
echo "Creating run.sh script..."

cat <<EOL > "$PROJECT_DIR/run.sh"
#!/bin/bash

# Activate the virtual environment (optional)
source /mnt/data/digivenv/bin/activate

# Start Django
exec env $(cat ./environment | xargs) python manage.py runserver 0.0.0.0:8005

EOL

# Make run.sh executable by everyone
chmod +x "$PROJECT_DIR/run.sh"
chmod a+x "$PROJECT_DIR/run.sh"  # This allows everyone to execute it

# Create the systemd service file
echo "Creating digital_attendance.service..."

cat <<EOL | sudo tee /etc/systemd/system/digital_attendance.service > /dev/null
[Unit]
Description=Digital Attendance Django Application (Django)
After=network.target

[Service]
ExecStart=$PROJECT_DIR/run.sh
WorkingDirectory=$PROJECT_DIR
Restart=always
EnvironmentFile=/etc/environment

[Install]
WantedBy=multi-user.target
EOL

# Reload systemd to apply the changes
echo "Reloading systemd..."
sudo systemctl daemon-reload

# Enable the service to start at boot
echo "Enabling digital_attendance service to start on boot..."
sudo systemctl enable digital_attendance

# Start the service
echo "Starting digital_attendance service..."
sudo systemctl start digital_attendance

# Show the status of the service
sudo systemctl status digital_attendance
