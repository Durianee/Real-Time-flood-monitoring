<template>
  <v-app>
    <v-app-bar app color="blue-darken-3" dark>
      <v-toolbar-title>🌊水位监测系统</v-toolbar-title>
    </v-app-bar>
    <v-main>
      <v-container fluid>
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
// 无额外逻辑
</script>

<style scoped>
/* 根据需要添加全局样式 */
</style>
