<template>
  <v-col cols="12" md="6" class="auth-left-section">
    <div class="logo-container">
      <img :src="logoSrc" :alt="logoAlt" class="auth-logo">
      <h2 class="auth-heading">
        <span v-html="title"></span>
        <span v-html="subtitle"></span>
      </h2>
    </div>
  </v-col>
</template>

<script>
export default {
  name: 'AuthLeftSection',

  props: {
    logoSrc: {
      type: String,
      required: true
    },
    logoAlt: {
      type: String,
      default: 'Logo'
    },
    title: {
      type: String,
      required: true
    },
    subtitle: {
      type: String,
      required: true
    }
  }
}
</script>
