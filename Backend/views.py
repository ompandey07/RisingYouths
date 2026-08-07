from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from .models import ContactMessage

def contact_us_view(request):
    if request.method == 'POST':
        try:
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            email = request.POST.get('email', '').strip()
            phone = request.POST.get('phone', '').strip()
            subject_key = request.POST.get('subject', '').strip()
            user_message = request.POST.get('message', '').strip()

            contact_obj = ContactMessage.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                subject=subject_key,
                message=user_message
            )

            # Send Email Notification to risingyouthsoverseas@gmail.com
            try:
                subject_display = contact_obj.get_subject_display()
                email_subject = f"[Contact Form] New Inquiry: {subject_display} from {first_name} {last_name}"
                
                # Plain Text Fallback
                text_content = (
                    f"New Contact Form Submission Received\n\n"
                    f"Name: {first_name} {last_name}\n"
                    f"Email: {email}\n"
                    f"Phone: {phone}\n"
                    f"Subject: {subject_display}\n\n"
                    f"Message:\n{user_message}\n\n"
                    f"---\nRising Youths Website Contact System"
                )

                # Formatted HTML Content
                html_content = f"""
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; border: 1px solid #e2e8f0; border-radius: 10px; overflow: hidden;">
                    <div style="background-color: #3b82f6; padding: 20px; text-align: center; color: white;">
                        <h2 style="margin: 0; font-size: 20px;">New Contact Form Message</h2>
                        <p style="margin: 5px 0 0 0; font-size: 13px; opacity: 0.9;">Rising Youths Overseas</p>
                    </div>
                    <div style="padding: 24px; background-color: #ffffff;">
                        <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
                            <tr>
                                <td style="padding: 8px 0; font-weight: bold; color: #475569; width: 120px;">Sender Name:</td>
                                <td style="padding: 8px 0; color: #1e293b;">{first_name} {last_name}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px 0; font-weight: bold; color: #475569;">Email:</td>
                                <td style="padding: 8px 0;"><a href="mailto:{email}" style="color: #2563eb;">{email}</a></td>
                            </tr>
                            <tr>
                                <td style="padding: 8px 0; font-weight: bold; color: #475569;">Phone:</td>
                                <td style="padding: 8px 0;"><a href="tel:{phone}" style="color: #1e293b; text-decoration: none;">{phone}</a></td>
                            </tr>
                            <tr>
                                <td style="padding: 8px 0; font-weight: bold; color: #475569;">Subject:</td>
                                <td style="padding: 8px 0;"><span style="background-color: #dbeafe; color: #1d4ed8; padding: 4px 10px; border-radius: 12px; font-size: 13px; font-weight: bold;">{subject_display}</span></td>
                            </tr>
                        </table>
                        
                        <div style="margin-top: 15px;">
                            <p style="font-weight: bold; color: #475569; margin-bottom: 8px;">Message:</p>
                            <div style="background-color: #f8fafc; border-left: 4px solid #3b82f6; padding: 14px; border-radius: 6px; color: #334155; line-height: 1.6; white-space: pre-wrap;">{user_message}</div>
                        </div>
                    </div>
                    <div style="background-color: #f1f5f9; padding: 12px 24px; text-align: center; font-size: 12px; color: #64748b;">
                        This email was sent automatically from the Rising Youths website contact form.
                    </div>
                </div>
                """

                recipient_email = getattr(settings, 'NOTIFY_EMAIL', 'risingyouthsoverseas@gmail.com')
                from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'risingyouthsoverseas@gmail.com')

                email_msg = EmailMultiAlternatives(
                    subject=email_subject,
                    body=text_content,
                    from_email=from_email,
                    to=[recipient_email]
                )
                email_msg.attach_alternative(html_content, "text/html")
                email_msg.send(fail_silently=True)

            except Exception as mail_err:
                print(f"Error sending email notification: {mail_err}")

            messages.success(request, "Your message has been sent successfully! We'll contact you soon.")
        except Exception as e:
            messages.error(request, "Something went wrong. Please try again.")
        return redirect('contact_us_view')
    return render(request, 'Modelpages/contact_us.html')




def error_acces_denied(request):
    """
    Render the unauthorized access/access denied page.
    Displays a stylish 403 error page with navigation options.
    """
    return render(request, 'Errors/UnAcess.html')



