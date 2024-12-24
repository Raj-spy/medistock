import asyncio
from datetime import datetime
from notificationapi_python_server_sdk import notificationapi

# Initialize NotificationAPI
notificationapi.init(
    "e9n119nm0ix2p8k57iqbj49lem",  # Replace with your clientId
    "vj6zmx09ki0tr3kb1rfjq0veqtq6yphiufseetgm3q9rhnh147bpw2zsk6"  # Replace with your clientSecret
)

# Mock database for medicines and users
users = [
    {
        "email": "traj96111@gmail.com",
        "phone": "+919755160469",
        "medicines": [
            {"name": "Paracetamol", "expiry_date": "2024-12-26"},
            {"name": "Ibuprofen", "expiry_date": "2024-12-27"}
        ]
    }
]

# Function to filter medicines expiring in 2 days
def get_expiring_medicines(user):
    today = datetime.now().date()  # Current date
    expiring_medicines = []

    for medicine in user["medicines"]:
        expiry_date = datetime.strptime(medicine["expiry_date"], "%Y-%m-%d").date()
        days_left = (expiry_date - today).days  # Calculate days until expiry

        if days_left == 2:  # If expiry is in 2 days
            expiring_medicines.append(medicine)

    return expiring_medicines

# Function to send a notification
async def send_notification(user_email, user_phone, medicine_name, expiry_date):
    # Notification message
    message = (
        f"Hello! A quick reminder: Your medicine '{medicine_name}' is about to expire on {expiry_date}. "
        f"Please ensure you take the necessary steps."
    )

    # Sending the notification using NotificationAPI
    await notificationapi.send({
        "notificationId": "alert",
        "user": {
            "id": user_email,
            "email": user_email,
            "number": user_phone
        },
        "mergeTags": {
            "message": message
        }
    })
    print(f"Notification sent to {user_email} for medicine '{medicine_name}'.")

# Main function to check and send notifications
async def check_and_notify(users):
    for user in users:
        expiring_medicines = get_expiring_medicines(user)

        for medicine in expiring_medicines:
            await send_notification(
                user_email=user["email"],
                user_phone=user["phone"],
                medicine_name=medicine["name"],
                expiry_date=medicine["expiry_date"]
            )

# Run the notification process
asyncio.run(check_and_notify(users))