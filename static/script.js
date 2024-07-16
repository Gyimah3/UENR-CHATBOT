// script.js

document.addEventListener('DOMContentLoaded', function() {
    // Chatbot functionality
    const chatbotToggler = document.querySelector(".chatbot-toggler");
    const chatbot = document.querySelector(".chatbot");
    const chatInput = chatbot.querySelector("textarea");
    const sendButton = chatbot.querySelector("#send-btn");

    chatbotToggler.addEventListener('click', function() {
        document.body.classList.toggle('show-chatbot');
    });

    sendButton.addEventListener('click', function() {
        if (chatInput.value.trim() !== '') {
            sendMessage(chatInput.value.trim());
            chatInput.value = '';
        }
    });

    chatInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage(this.value);
            this.value = '';
        }
    });

    function sendMessage(message) {
        const chatBox = chatbot.querySelector(".chatbox");
        const userMessageElement = createUserMessageElement(message);
        chatBox.appendChild(userMessageElement);
        chatBox.scrollTop = chatBox.scrollHeight;

        fetchChatbotResponse(message, function(botMessage) {
            typeWriterEffect(botMessage, chatBox);
        });
    }

    function fetchChatbotResponse(message, callback) {
        const sanitizedMessage = sanitizeInput(message);

        fetch('/api/message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: sanitizedMessage }),
        })
        .then(response => response.json())
        .then(data => {
            callback(data.response);
        })
        .catch(error => {
            console.error('Error:', error);
            callback('Sorry, I am unable to respond at the moment. Please try again later.');
        });
    }

    function createBotMessageElement() {
        const element = document.createElement('li');
        element.classList.add('chat', 'incoming');
        element.innerHTML = `
            <img src="https://newsnowgh.com/wp-content/uploads/2020/11/University-of-Energy-and-Natural-Resources-UENR.jpg" alt="UENR Logo" class="bot-icon">
            <p></p>
        `;
        return element;
    }

    function createUserMessageElement(message) {
        const element = document.createElement('li');
        element.classList.add('chat', 'outgoing');
        element.innerHTML = `
            <p>${sanitizeInput(message)}</p>
            <span class="material-icons user-icon">person</span>
        `;
        return element;
    }
    
    function sanitizeInput(input) {
        return input.replace(/</g, "&lt;").replace(/>/g, "&gt;");
    }
    
    function typeWriterEffect(message, chatBox) {
        const botMessageElement = createBotMessageElement();
        chatBox.appendChild(botMessageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
    
        const textElement = botMessageElement.querySelector('p');
        let index = 0;
        const speed = 10; // Typing speed in milliseconds per character
    
        function typeWriter() {
            if (index < message.length) {
                textElement.innerHTML += message.charAt(index);
                index++;
                setTimeout(typeWriter, speed); // Adjust typing speed here (milliseconds per character)
                chatBox.scrollTop = chatBox.scrollHeight;
            }
        }
    
        typeWriter();
    }
    
    // Slideshow and section display functionality
    let sectionIndex = 0;
    let slideIndex = 0;
    const sections = document.querySelectorAll('main .info-section');
    const slideInterval = 3000; // 3 seconds for each slide
    const sectionInterval = slideInterval * 3; // 3 slides per section
    
    showSection();
    
    function showSection() {
        if (sectionIndex < sections.length) {
            const currentSection = sections[sectionIndex];
            currentSection.classList.add('active');
            const slides = currentSection.querySelectorAll('.slideshow-container img');
    
            showSlides(slides, () => {
                currentSection.classList.remove('active');
                sectionIndex++;
                if (sectionIndex >= sections.length) {
                    sectionIndex = 0; // Reset to the first section
                }
                showSection();
            });
        }
    }
    
    function showSlides(slides, callback) {
        let slideShowIndex = 0;
    
        function showNextSlide() {
            slides.forEach(slide => slide.classList.remove('active-slide'));
            slides[slideShowIndex].classList.add('active-slide');
            slideShowIndex++;
    
            if (slideShowIndex < slides.length) {
                setTimeout(showNextSlide, slideInterval);
            } else {
                setTimeout(callback, slideInterval);
            }
        }
    
        showNextSlide();
    }
});    





// // script.js

// // Event listeners for chatbot interactions
// document.addEventListener('DOMContentLoaded', function() {
//     const chatbotToggler = document.querySelector(".chatbot-toggler");
//     const chatbot = document.querySelector(".chatbot");
//     const chatInput = chatbot.querySelector("textarea");
//     const sendButton = chatbot.querySelector("#send-btn");

//     chatbotToggler.addEventListener('click', function() {
//         document.body.classList.toggle('show-chatbot');
//     });

//     // Update the event listener for the send button
//     sendButton.addEventListener('click', function() {
//         if (chatInput.value.trim() !== '') {
//             sendMessage(chatInput.value.trim());
//             chatInput.value = '';
//         }
//     });
   

//     chatInput.addEventListener('keypress', function(e) {
//         if (e.key === 'Enter' && !e.shiftKey) {
//             e.preventDefault();
//             sendMessage(this.value);
//             this.value = '';
//         }
//     });

//     function sendMessage(message) {
//         const chatBox = chatbot.querySelector(".chatbox");
//         const userMessageElement = createUserMessageElement(message);
//         chatBox.appendChild(userMessageElement);
//         chatBox.scrollTop = chatBox.scrollHeight;

//         fetchChatbotResponse(message, function(botMessage) {
//             const botMessageElement = createBotMessageElement(botMessage);
//             chatBox.appendChild(botMessageElement);
//             chatBox.scrollTop = chatBox.scrollHeight;
//         });
//     }

//     function fetchChatbotResponse(message, callback) {
//         const sanitizedMessage = sanitizeInput(message);

//         fetch('/api/message', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//             },
//             body: JSON.stringify({ message: sanitizedMessage }),
//         })
//         .then(response => response.json())
//         .then(data => {
//             // Now using the callback to handle the response
//             callback(data.response); // Make sure 'data.response' matches the server's response structure
//         })
//         .catch(error => {
//             console.error('Error:', error);
//             callback('Sorry, I am unable to respond at the moment. Please try again later.');
//         });
//     }

//     // Ensure this function is defined at the top level within the DOMContentLoaded event handler
//     function createBotMessageElement(message) {
//         const element = document.createElement('li');
//         element.classList.add('chat', 'incoming');
//         element.innerHTML = `
//             <span class="material-icons">android</span>
//             <p>${message}</p>
//         `;
//         return element;
//     }
    

//     function createUserMessageElement(message) {
//     const element = document.createElement('li');
//     element.classList.add('chat', 'outgoing');
//     element.innerHTML = `
//         <p>${sanitizeInput(message)}</p>
//         <span class="material-icons user-icon">person</span>
//     `;
//     return element;
//     }


//     function sanitizeInput(input) {
//         return input.replace(/</g, "&lt;").replace(/>/g, "&gt;");
//     }
// });
