console.log('Content js check (interact with page)');

function findBaitAndSwitch() {
    // Select all clickable elements on the page
    const clickableElements = document.querySelectorAll('a, button, input[type="submit"], [role="button"]');
    // Iterate through each clickable element
    clickableElements.forEach(element => {
      // Check if the element triggers a navigation or change in content
      element.addEventListener('click', function() {
        // You may want to customize this part based on the specifics of bait and switch you are looking for
        // Here, it checks if the element's href or associated action is different after the click
        if (element.href && element.href !== document.location.href) {
          console.log(`Potential bait and switch detected: ${element.textContent}`);
          // You can take further actions, like marking the element or notifying the user
          element.style.border = '2px solid red';
        } else if (element.form && element.form.action && element.form.action !== document.location.href) {
          console.log(`Potential bait and switch detected: ${element.textContent}`);
          element.style.border = '2px solid red';
        }
      });
    });
  }
  // Call the function when the page is fully loaded
  window.addEventListener('load', findBaitAndSwitch);

  function detectMisdirection() {
    // Select all clickable elements on the page
    const clickableElements = document.querySelectorAll('a, button, [role="button"], input[type="submit"]');
  
    // Iterate through each clickable element
    clickableElements.forEach(element => {
      // Attach a click event listener to each element
      element.addEventListener('click', () => {
        // Check if the element has an href attribute
        if (element.href) {
          // Get the destination URL
          const destinationURL = element.href;
  
          // Check if the destination URL is different from the current URL
          if (destinationURL !== window.location.href) {
            console.log(`Potential misdirection detected: ${element.textContent}`);
            // You can take further actions, like marking the element or notifying the user
            element.style.border = '2px solid red';
            // Optionally, prevent the default behavior to stop the navigation
            // event.preventDefault();
          }
        }
      });
    });
  }
  
  // Call the function when the page is fully loaded
  window.addEventListener('load', detectMisdirection);

  function detectPrivacyZuckering() {
    // Select elements that might be associated with privacy settings or data collection
    const privacyElements = document.querySelectorAll('[data-privacy], [data-consent], [data-tracking], [data-analytics]');
  
    // Iterate through each privacy-related element
    privacyElements.forEach(element => {
      // Check for attributes indicating potential privacy zuckering
      if (element.hasAttribute('data-privacy') || element.hasAttribute('data-consent') || element.hasAttribute('data-tracking') || element.hasAttribute('data-analytics')) {
        console.log(`Potential privacy zuckering detected: ${element.outerHTML}`);
        // You can take further actions, like marking the element or notifying the user
        element.style.border = '2px solid red';
      }
    });
  }
  
  // Call the function when the page is fully loaded
  window.addEventListener('load', detectPrivacyZuckering);

  function detectTrickyQuestions() {
    // Select form elements that might be associated with tricky questions
    const formElements = document.querySelectorAll('input[type="text"], input[type="password"], input[type="email"], textarea');
  
    // Iterate through each form element
    formElements.forEach(element => {
      // Check for characteristics indicating potential tricky questions
      if (isTrickyQuestion(element)) {
        console.log(`Potential tricky question detected: ${element.outerHTML}`);
        // You can take further actions, like marking the element or notifying the user
        element.style.border = '2px solid red';
      }
    });
  }
  
  // Function to check characteristics of a form element indicating potential tricky questions
  function isTrickyQuestion(element) {
    // Example: Check if the input's label contains specific terms like "free" or "trial"
    const label = document.querySelector(`label[for="${element.id}"]`);
    if (label && (label.textContent.toLowerCase().includes('free') || label.textContent.toLowerCase().includes('trial'))) {
      return true;
    }
  
    // You may need to customize this function based on specific characteristics of tricky questions you are looking for
    return false;
  }
  
  