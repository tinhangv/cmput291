# Check if there are more followers to display beyond the current page
if start_index + flwer_count < len(flwer_list):
    print("\nOptions: Type 'N' to see the Next page or 'B' to go Back.")
else:
    print("\nOptions: Type 'B' to go Back.")

#user input to select option
choice = input("Choose an option: ").strip().upper()
if choice == "N" and start_index + flwer_count < len(flwer_list):
    # Move to the next set of rows by updating start_index
    start_index += flwer_count
elif choice == "B":
    break  # Exit the follower list view
else:
    print("Invalid choice. Try again.")