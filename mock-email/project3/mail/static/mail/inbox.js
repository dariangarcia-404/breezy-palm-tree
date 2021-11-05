document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').addEventListener('submit', (event) => send_email(event));

  // By default, load the inbox
  load_mailbox('inbox');
});

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#message-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => emails.forEach(email => {
    const email_template = document.createElement('div');
    email_template.classList.add('email-template');
    var div_class = "";
    if(email.read === true) {
      div_class = "<div class=\"read\">";
    }
    else {
      div_class = "<div class=\"unread\">";
    }
    email_template.innerHTML = `${div_class} <b>${email.sender}</b> ${email.subject} <span class='email-timestamp'>${email.timestamp}</span> </div>`;
    email_template.addEventListener('click', () => show_email(email.id));
    document.querySelector('#emails-view').append(email_template);
  })
  );

}

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#message-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

}

function show_email(email_id) {

  document.querySelector('#message-view').style.display = 'block';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  document.querySelector('#message-contents').innerHTML = '';
  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
    console.log(email);
    var archive_btn = document.querySelector('#archive-btn');
    var reply_btn = document.querySelector('#reply-btn');
    if (email.archived) {
      archive_btn.value = 'Unarchive';
    }
    else {
      archive_btn.value = 'Archive';
    }
    archive_btn.addEventListener('click', () => archive_email(email.id));
    reply_btn.addEventListener('click', () => reply_email(email.id));
    const email_template = document.createElement('div');
    email_template.classList.add('email-template');
    email_template.innerHTML = `<b>From: </b>${email.sender} \n<br>\n <b>To: </b>${email.recipients} \n<br>\n <b>Subject: </b>${email.subject} \n<br>\n <b>Timestamp: </b><span>${email.timestamp}</span> \n<br>\n <hr> <p>${email.body}</p>`;
    document.querySelector('#message-contents').append(email_template);
  });

  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  })

}

function reply_email(email_id) {
  // Show compose view and hide other views
  document.querySelector('#message-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
    document.querySelector('#compose-recipients').value = email.sender;
    if (!email.subject.startsWith('Re:')) {
      document.querySelector('#compose-subject').value = 'Re: ' + email.subject;
    }
    else {
      document.querySelector('#compose-subject').value = email.subject;
    }
    document.querySelector('#compose-body').value = `\n\nOn ${email.timestamp}, ${email.sender} wrote: \n ${email.body}`;
  });

}

function archive_email(email_id) {
  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
    var archive_btn = document.querySelector('#archive-btn');
    var now_archived = true; // should it be archived now?
    archive_btn.value = "Unarchive";
    if (email.archived === true) {
      now_archived = false; // if it is, switch to not.
      archive_btn.value = "Archive";
    }
    fetch(`/emails/${email_id}`, {
      method: 'PUT',
      body: JSON.stringify({
        archived: now_archived
      })
    })
  });

}

function send_email(event) {
  event.preventDefault()
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body,
      read: false
    })
  })
  .then(response => response.json())
  .then(result => { console.log(result); });

  alert("Email sent.");
  load_mailbox('sent');
}
