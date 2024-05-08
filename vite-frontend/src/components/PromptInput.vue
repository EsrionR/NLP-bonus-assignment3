<template>
  <div>
    <div v-if="formSubmitted">
      <hr />
      <p>prompt: {{ prompt }}</p>
      <div v-if="answer">
        <!-- <p v-bind:src="response" >{{ response }}</p> -->
        <p>{{ response }}</p>
      </div>
      <div v-else>
        <h2>hmm...</h2>
      </div>
    </div>

    <form @submit.prevent="submitForm">
      <br />
      <input
        type="text"
        v-model="prompt"
        placeholder="Input the prompt"
        required
      />
      <br /><br />
      <button type="submit" class="submit button" role="button">
        Submit
      </button>
    </form>
  </div>
</template>


<script>
export default {
  data() {
    return {
      prompt: "",
      formSubmitted: false,
      answer: null,
    };
  },

  methods: {
    async submitForm() {
      this.formSubmitted = true;
      try {
        // const response = await fetch("http://127.0.0.1:8000/ai/" + this.prompt);
        // const data = await response.json();
        // console.log(data);

        // // Loop through each answer in the JSON response
        // for (const key in data) {
        //   if (data.hasOwnProperty(key)) {
        //     const answer = data[key];
        //     console.log(answer);
        //     // Display each answer in the template as desired
        //     // For example:
        //     console.log("Question:", answer.question);
        //     console.log("Answer:", answer.answer);
        //   }
        // }
        fetch("http://127.0.0.1:8000/ai/" + this.prompt)
          .then((response) => {
            console.log(response);
            return response.json();
          })
          .then((data) => {
            // this.answer = data["answer"];
            // console.log(data);
            // for (const key in data) {
            //   if (data.hasOwnProperty(key)) {
            //     this.answer = data[key]["answer"];
            //     console.log(this.answer);
            //   }
            //   this.answer = "test";
            // }
            
            const data2 = JSON.parse(data);
            const keys = Object.keys(data2);
            const lastKey = keys[keys.length - 1];
            console.log(lastKey);
            console.log(data2[lastKey]);
            console.log(data2[lastKey]["answer"]);
            this.answer = data2[lastKey]["answer"];
            console.log(this.answer);
          });
      } catch (error) {
        console.error("Error:", error);
      }
    },
  },

  computed: {
    response() {
      return this.answer;
    },
  },
};
</script>

<style scoped>



</style>