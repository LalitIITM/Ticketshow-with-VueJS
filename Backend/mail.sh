#! /bin/sh
echo "======================================================================"
echo "Welcome to to the app. This will setup the mailhog" 

echo "You can rerun this without any issues."
echo "----------------------------------------------------------------------"
# Measure the time before installing Python libraries
start_time=$(date +%s)

# Run MailHog from new terminal
cd /mnt/d/MailHog #we can change it by putting MailHog inside project directory 
#and run from there
./mailhog

end_time=$(date +%s)

# Calculate and display the elapsed time
elapsed_time=$((end_time - start_time))
echo "Installation completed in $elapsed_time seconds."

end_time=$(date +%s)

# Calculate and display the elapsed time
elapsed_time=$((end_time - start_time))
echo "completed in $elapsed_time seconds."
