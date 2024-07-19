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
    echo "Enabling virtual env"
else
    echo "No Virtual env. Please run setup.sh first"
    exit N
fi

# Activate virtual env
. .env/bin/activate
export ENV=development
end_time=$(date +%s)

# Calculate and display the elapsed time
elapsed_time=$((end_time - start_time))
echo "Virtual Environment activated in $elapsed_time seconds."

python3 main.py
deactivate

