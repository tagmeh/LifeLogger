from unittest.mock import patch, call

import pytest
from django.core.mail import send_mail

from user.models import ExtendedUser


# @pytest.mark.django_db
# def test_send_reminder():
#     user = ExtendedUser.objects.create_user(
#         username='testuser', email='testuser@example.com', password='password'
#     )
#     with patch.object(send_mail, 'delay') as mock_send_mail:
#         user.send_reminder()
#
#         assert mock_send_mail.call_count == 1
#         assert mock_send_mail.call_args == call(
#             subject="Don't forget to update your habits!",
#             message="Howdy, be sure to stop by LifeLogger and update the progress on your habits!\nHabits:\nhabit1",
#             from_email="LifeLogger@life.com",
#             recipient_list=["testuser@example.com"],
#         )
