# Budget Tracking Web App
#### Video Demo:  <URL HERE>
#### Description:
Hey there! Welcome to my Budget Tracker Web App, a project created for Harvard's CS50x course.

## Why Build This?

I decided to build my own backend for this project because Supabase, while powerful, was a bit challenging to integrate with Python. This gave me the perfect opportunity to deepen my understanding of Flask and SQLAlchemy. Plus, the entire app runs smoothly on my Docker server and exposed with traefik on my own doamin with full tls and valid ssl certificates using Let's Encrypt and Cloudflare, helping me learn more about containarization and certificates.

Here is my failed attemp to integrate supabase baas to this project: https://github.com/KJJisBetter/budget-webapp. Also my first project attempt for CS50x, a machine monitoring but in c: https://github.com/KJJisBetter/monitoring.

I have my own homelab with a lot of services.

## Challenges and Lessons Learned

One of the biggest challenges was ensuring the accurate aggregation of transaction data for the charts. Debugging involved verifying data at each step, from the database query to the frontend rendering. This process was a great learning experience and helped me understand the importance of data integrity.

In the future, I plan to add more features such as budget goals, alerts for overspending, and integration with external APIs for real-time data.