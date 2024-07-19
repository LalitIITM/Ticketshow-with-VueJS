#! /bin/sh
echo "======================================================================"
echo "Welcome to to the Frontend run." 
echo "And then it will install all the required dependencies."
echo "You can rerun this without any issues."
echo "----------------------------------------------------------------------"
# Measure the time before installing Python libraries
start_time=$(date +%s)

yarn install

# Calculate and display the elapsed time
elapsed_time=$((end_time - start_time))
echo "Yarn installed in $elapsed_time seconds."

yarn serve





