<script setup>
import PromptInput from './components/PromptInput.vue';

const components = {
  PromptInput,
};

</script>

<template>
  <div id="app">
    <div class="container">
      <div class="header">
        <!-- Your header content goes here -->
        <h1>Tulip Talks</h1>
      </div>
      <div class="welcome">
        <p>Hi! Welcome to Tulip Talks! Ask me anything.</p>
        <p> I am a Dutch AI Language Coach, Tulip Talks. We will learn Dutch by role-playing common scenarios to get you familiar with the language. 
          You can type anything in the chatbox, and everything will be explained step by step. 
          Let’s get started and have some fun! </p>
      </div>
      <div class="chat-output">
        <h1>Chat</h1>
        <!-- Your chat output goes here -->
      </div>
      <div class="chat-input">
        <PromptInput />
      </div>
    </div>
  </div>
</template>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.header {
  /* Adjust as needed */
  padding: 1em;
}

.chat-output {
  flex-grow: 1;
  overflow-y: auto;
  padding: 1em;
}

.chat-input {
  padding: 1em;
}
</style>