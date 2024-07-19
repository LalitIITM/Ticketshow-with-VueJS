#! /bin/sh
echo "======================================================================"
echo "Welcome to to the setup. This will setup the local virtual env." 
echo "And then it will install all the required python libraries."
echo "You can rerun this without any issues."
echo "----------------------------------------------------------------------"
# Measure the time before installing Python libraries
start_time=$(date +%s)

if [ -d ".env" ];
then
    echo ".env folder exists. Installing using pip"
else
    echo "creating .env and install using pip"
    python3.10 -m venv .env
fi

# Activate virtual env
. .env/bin/activate

# Upgrade the PIP
#echo "Upgrading PIP..."
#pip install --upgrade pip
#echo "Installing Python libraries from requirements.txt..."
pip install -r requirements.txt

end_time=$(date +%s)

# Calculate and display the elapsed time
elapsed_time=$((end_time - start_time))
echo "Installation completed in $elapsed_time seconds."
# Work done. so deactivate the virtual env
deactivate
