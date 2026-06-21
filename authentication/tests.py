from django.test import TestCase
from django.contrib.auth import get_user_model, authenticate
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class CustomUserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test_student',
            email='test@college.edu',
            password='testpassword123',
            full_name='Test Student',
            role='Student',
            college='IIT Delhi'
        )

    def test_user_creation(self):
        """Verify fields are assigned correctly on creation."""
        self.assertEqual(self.user.username, 'test_student')
        self.assertEqual(self.user.email, 'test@college.edu')
        self.assertEqual(self.user.role, 'Student')
        self.assertFalse(self.user.is_verified)

    def test_otp_generation_and_validation(self):
        """Verify OTP is generated, expires correctly, and validates successfully."""
        otp = self.user.generate_otp()
        self.assertEqual(len(otp), 6)
        self.assertTrue(self.user.is_otp_valid(otp))
        
        # Test expired OTP
        self.user.otp_expiry = timezone.now() - timedelta(minutes=1)
        self.user.save()
        self.assertFalse(self.user.is_otp_valid(otp))

    def test_lockout_mechanism(self):
        """Verify failed login attempts increment and trigger lockout correctly."""
        self.assertFalse(self.user.is_locked_out())
        
        # Simulate 5 failed attempts
        for _ in range(5):
            self.user.increment_failed_attempts()
            
        self.assertTrue(self.user.is_locked_out())
        self.assertEqual(self.user.failed_login_attempts, 5)
        
        # Test reset
        self.user.reset_failed_attempts()
        self.assertFalse(self.user.is_locked_out())
        self.assertEqual(self.user.failed_login_attempts, 0)

    def test_email_or_username_backend(self):
        """Verify authentication works with both username and email address."""
        # Authenticate via username
        user_by_username = authenticate(username='test_student', password='testpassword123')
        self.assertEqual(user_by_username, self.user)
        
        # Authenticate via email
        user_by_email = authenticate(username='test@college.edu', password='testpassword123')
        self.assertEqual(user_by_email, self.user)
        
        # Fail with wrong password
        user_fail = authenticate(username='test_student', password='wrongpassword')
        self.assertIsNone(user_fail)
