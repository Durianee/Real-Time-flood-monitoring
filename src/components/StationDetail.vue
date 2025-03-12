<template>
  <v-container fluid>
    <v-btn text @click="$router.push('/')">Back to List</v-btn>
    <v-card class="mb-4" outlined v-if="station && station.label">
      <v-card-title>{{ station.label }} ({{ station.riverName }})</v-card-title>
      <v-card-text>
        <div><strong>City:</strong> {{ station.town }}</div>
        <div><strong>Date Opened:</strong> {{ station.dateOpened }}</div>
        <div><strong>Status:</strong> {{ station.status }}</div>
        <div><strong>Catchment:</strong> {{ station.catchmentName }}</div>
        <div><strong>Coordinates:</strong> {{ station.lat }}, {{ station.long }}</div>
      </v-card-text>
    </v-card>

    <!-- Time range toggle (supports 24h and 7d) -->
    <v-btn-toggle v-model="period" color="primary" class="mb-4" mandatory>
      <v-btn value="24h">24h</v-btn>
      <v-btn value="7d">7d</v-btn>
    </v-btn-toggle>

    <!-- Line chart section -->
    <v-card v-if="readings && readings.length > 0" outlined class="mb-4 pa-4">
      <canvas ref="chartCanvas"></canvas>
    </v-card>
    <v-alert v-else type="info" elevation="2">
      No historical readings data available
    </v-alert>

    <!-- Historical readings data table -->
    <v-card v-if="readings && readings.length > 0" outlined>
      <v-card-title>Historical Readings Data</v-card-title>
      <v-data-table :items="readings" :headers="tableHeaders" :items-per-page="10" class="elevation-1" dense>
        <template v-slot:item.dateTime="{ item }">
          {{ formatDate(item.dateTime) }}
        </template>
        <template v-slot:item.value="{ item }">
          {{ item.value.toFixed(2) }}
          {{ station.measures && station.measures.length > 0 ? station.measures[0].unitName : 'm' }}
        </template>
      </v-data-table>
    </v-card>

    <!-- Loading indicator -->
    <v-container v-if="!station || !station.label" class="text-center">
      <v-progress-circular indeterminate color="primary"></v-progress-circular>
    </v-container>
  </v-container>
</template>

<script>
import axios from 'axios';
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);

export default {
  name: 'StationDetail',
  props: ['id'],
  data() {
    return {
      station: {},
      readings: [],
      period: '24h', // Default is 24h
      chart: null,
      tableHeaders: [
        { text: 'Time', value: 'dateTime', sortable: true },
        { text: 'Water Level', value: 'value', sortable: true }
      ]
    }
  },
  mounted() {
    console.log("StationDetail id:", this.id);
    this.fetchStationData();
  },
  watch: {
    period(newVal, oldVal) {
      if (newVal !== oldVal) {
        this.fetchStationData();
      }
    },
    readings(newVal) {
      this.$nextTick(() => {
        if (this.$refs.chartCanvas) {
          this.updateChart();
        } else {
          console.warn("chartCanvas not rendered!");
        }
      });
    }
  },
  methods: {
    fetchStationData() {
      // Fetch station details
      this.$axios.get(`/api/station/${this.id}`)
        .then(res => {
          console.log("Station detail response:", res.data);
          if (res.data.items && res.data.items.length > 0) {
            this.station = res.data.items[0];
          } else {
            this.station = res.data;
          }
        })
        .catch(err => {
          console.error("Error fetching station detail:", err);
        });
      
      // Fetch historical readings data
      this.$axios.get(`/api/readings/${this.id}?period=${this.period}`)
        .then(res => {
          console.log("Readings response:", res.data);
          this.readings = res.data;
        })
        .catch(err => {
          console.error("Error fetching readings:", err);
        });
    },
    updateChart() {
      if (!this.$refs.chartCanvas) {
        console.error("chartCanvas not found");
        return;
      }
      if (this.chart) {
        this.chart.destroy();
      }
      const ctx = this.$refs.chartCanvas.getContext('2d');
      const labels = this.readings.map(r => this.formatTimeLabel(r.dateTime));
      const values = this.readings.map(r => r.value);
      console.log("Chart labels:", labels);
      console.log("Chart values:", values);
      this.chart = new Chart(ctx, {
        type: 'line',
        data: {
          labels,
          datasets: [{
            label: 'Water Level',
            data: values,
            fill: false,
            borderColor: '#1976D2',
            tension: 0.1,
            pointRadius: 3,
          }]
        },
        options: {
          scales: {
            x: { display: true, title: { display: true, text: 'Time' } },
            y: { display: true, title: { display: true, text: `Water Level (${this.station.measures && this.station.measures.length > 0 ? this.station.measures[0].unitName : 'm'})` } }
          },
          plugins: {
            tooltip: { mode: 'nearest' },
            legend: { display: false }
          }
        }
      });
    },
    formatTimeLabel(dateTimeStr) {
      const dt = new Date(dateTimeStr);
      if (this.period === '24h') {
        return dt.getHours() + ':00';
      } else {
        return (dt.getMonth() + 1) + "-" + dt.getDate();
      }
    },
    formatDate(dateTimeStr) {
      const dt = new Date(dateTimeStr);
      const Y = dt.getFullYear(), M = dt.getMonth() + 1, D = dt.getDate();
      const h = dt.getHours(), m = dt.getMinutes();
      return `${Y}-${M < 10 ? '0' + M : M}-${D < 10 ? '0' + D : D} ${h < 10 ? '0' + h : h}:${m < 10 ? '0' + m : m}`;
    }
  }
};
</script>


