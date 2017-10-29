function addContact(value) {
  if (value === 3) {
    console.log("You ran number 3");
    // form_data = document.getElementsByClassName("third-contact-box");
    // new_name = form_data[0].value;
    // new_phone = form_data[1].value;
    // new_email = form_data[2].value;
    // document.getElementsByClassName("contact-box-3-name")[0].innerHTML = new_name;
    // document.getElementsByClassName("contact-box-3-number")[0].innerHTML = new_phone;
    // document.getElementsByClassName("contact-box-3-email")[0].innerHTML = new_email;
    // document.getElementsByClassName("contact-card3")[0].classList.remove("ensure-hidden");
    document.getElementsByClassName("contact-form3")[0].classList.add("ensure-hidden");
  } else if (value === 4) {
    console.log("You ran number 4");
    // form_data = document.getElementsByClassName("fourth-contact-box");
    // new_name = form_data[0].value;
    // new_phone = form_data[1].value;
    // new_email = form_data[2].value;
    // document.getElementsByClassName("contact-box-4-name")[0].innerHTML = new_name;
    // document.getElementsByClassName("contact-box-4-number")[0].innerHTML = new_phone;
    // document.getElementsByClassName("contact-box-4-email")[0].innerHTML = new_email;
    // document.getElementsByClassName("contact-card4")[0].classList.remove("ensure-hidden");
    document.getElementsByClassName("contact-form4")[0].classList.add("ensure-hidden");
  } else {
    console.log("Something went wrong...");
    return;
  }
  return;
}
