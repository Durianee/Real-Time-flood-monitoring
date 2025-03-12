<template>
  <v-container fluid>
    <v-btn text @click="$router.push('/')">返回列表</v-btn>
    <v-card class="mb-4" outlined v-if="station && station.label">
      <v-card-title>{{ station.label }} ({{ station.riverName }})</v-card-title>
      <v-card-text>
        <div><strong>城市：</strong> {{ station.town }}</div>
        <div><strong>开站日期：</strong> {{ station.dateOpened }}</div>
        <div><strong>状态：</strong> {{ station.status }}</div>
        <div><strong>集水区：</strong> {{ station.catchmentName }}</div>
        <div><strong>经纬度：</strong> {{ station.lat }}, {{ station.long }}</div>
      </v-card-text>
    </v-card>

    <!-- 时间范围切换按钮（仅支持 24h 和 7d） -->
    <v-btn-toggle v-model="period" color="primary" class="mb-4" mandatory>
      <v-btn value="24h">24小时</v-btn>
      <v-btn value="7d">7天</v-btn>
    </v-btn-toggle>

    <!-- 折线图区域 -->
    <v-card v-if="readings && readings.length > 0" outlined class="mb-4 pa-4">
      <canvas ref="chartCanvas"></canvas>
    </v-card>
    <v-alert v-else type="info" elevation="2">
      暂无历史读数数据
    </v-alert>

    <!-- 历史读数数据表 -->
    <v-card v-if="readings && readings.length > 0" outlined>
      <v-card-title>历史读数数据</v-card-title>
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

    <!-- 加载指示器 -->
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
      period: '24h',  // 默认选择 24 小时
      chart: null,
      tableHeaders: [
        { text: '时间', value: 'dateTime', sortable: true },
        { text: '水位', value: 'value', sortable: true }
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
          console.warn("chartCanvas 未渲染！");
        }
      });
    }
  },
  methods: {
    fetchStationData() {
      // 获取站点详细信息
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
      
      // 获取历史读数数据
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
        console.error("chartCanvas 未找到");
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
            label: '水位值',
            data: values,
            fill: false,
            borderColor: '#1976D2',
            tension: 0.1,
            pointRadius: 3,
          }]
        },
        options: {
          scales: {
            x: { display: true, title: { display: true, text: '时间' } },
            y: { display: true, title: { display: true, text: `水位 (${this.station.measures && this.station.measures.length > 0 ? this.station.measures[0].unitName : 'm'})` } }
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

<style scoped>
/* 根据需要添加样式 */
</style>
