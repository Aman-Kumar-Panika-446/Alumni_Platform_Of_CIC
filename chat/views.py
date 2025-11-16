from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Max
from authentication.models import CustomUser
from .models import Message

@login_required
def get_contact_list(user):
    """
    Returns a list of unique contacts the user has chatted with,
    sorted by the latest message timestamp.
    """
    # Get all messages involving the user
    last_msgs = (
        Message.objects.filter(Q(sender=user) | Q(receiver=user))
        .values("sender", "receiver")
        .annotate(last_time=Max("timestamp"))
        .order_by("-last_time")
    )

    contact_dict = {}  # store unique contact with latest message

    for entry in last_msgs:
        sender_id = entry["sender"]
        receiver_id = entry["receiver"]

        # Identify the other user
        other_user_id = receiver_id if sender_id == user.id else sender_id

        # If we already added this contact, skip
        if other_user_id in contact_dict:
            continue

        # Get the last message for this pair (one query per contact)
        last_msg = (
            Message.objects.filter(
                Q(sender_id=sender_id, receiver_id=receiver_id)
                | Q(sender_id=receiver_id, receiver_id=sender_id)
            )
            .order_by("-timestamp")
            .first()
        )

        if last_msg:
            contact = last_msg.receiver if last_msg.sender == user else last_msg.sender
            contact_dict[other_user_id] = {
                "user": contact,
                "last_message": last_msg,
            }

    # Sort contacts by latest message timestamp
    contact_list = sorted(
        contact_dict.values(), key=lambda x: x["last_message"].timestamp, reverse=True
    )
    return contact_list


@login_required
def chat_view(request):
    """
    Sidebar view showing list of unique contacts with latest messages.
    """
    contact_list = get_contact_list(request.user)
    return render(request, "chat/chat.html", {"user_last_messages": contact_list})


@login_required
def chat_room(request, username):
    """
    Chat room view showing messages between current user and selected user.
    """
    receiver = get_object_or_404(CustomUser, username=username)
    user = request.user

    # Fetch chat messages between both users
    chats = (
        Message.objects.filter(Q(sender=user, receiver=receiver) | Q(sender=receiver, receiver=user))
        .order_by("timestamp")
    )

    # Sidebar contacts (reuse helper)
    contact_list = get_contact_list(user)

    context = {
        "room_name": receiver.username,
        "slug": receiver.username,
        "receiver": receiver,
        "chats": chats,
        "user_last_messages": contact_list
    }
    return render(request, "chat/chat.html", context)
