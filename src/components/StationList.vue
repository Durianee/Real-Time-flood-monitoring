<template>
  <v-container fluid>
    <v-card outlined class="mb-4">
      <v-card-title>Station List</v-card-title>
      <v-card-text>
        <!-- Search box -->
        <v-text-field v-model="searchTerm" label="Search (Station Name, City, River)" clearable></v-text-field>
        <!-- Grouping selection -->
        <v-select v-model="groupBy" :items="groupOptions" label="Group By" @change="onGroupByChange"></v-select>
      </v-card-text>
      <v-divider></v-divider>
      <v-expansion-panels>
        <v-expansion-panel v-for="(group, key) in groupedStations" :key="key">
          <v-expansion-panel-title>
            {{ key }} ({{ group.length }})
          </v-expansion-panel-title>
          <v-expansion-panel-text>
            <v-list dense>
              <v-list-item
                v-for="station in group"
                :key="station.stationReference"
                @click="goDetail(station)"
                style="cursor: pointer;"
              >
                <v-list-item-title>{{ station.label }}</v-list-item-title>
                <v-list-item-subtitle>
                  {{ station.town }} | {{ station.riverName }}
                </v-list-item-subtitle>
              </v-list-item>
            </v-list>
          </v-expansion-panel-text>
        </v-expansion-panel>
      </v-expansion-panels>
    </v-card>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  name: 'StationList',
  data() {
    return {
      stations: [],
      searchTerm: '',
      groupBy: 'riverName', // Default group by riverName
      groupOptions: ['riverName', 'town']
    };
  },
  mounted() {
    this.fetchStations();
  },
  computed: {
    // Filter stations by search keyword
    filteredStations() {
      if (!this.searchTerm) return this.stations;
      const term = this.searchTerm.toLowerCase();
      return this.stations.filter(station =>
        (station.label && station.label.toLowerCase().includes(term)) ||
        (station.town && station.town.toLowerCase().includes(term)) ||
        (station.riverName && station.riverName.toLowerCase().includes(term))
      );
    },
    // Group stations by the groupBy field
    groupedStations() {
      const groups = {};
      this.filteredStations.forEach(station => {
        const key = station[this.groupBy] || 'Other';
        if (!groups[key]) {
          groups[key] = [];
        }
        groups[key].push(station);
      });
      return groups;
    }
  },
  methods: {
    fetchStations() {
      this.$axios.get('/api/stations')
        .then(res => {
          this.stations = res.data;
        })
        .catch(err => {
          console.error("Failed to fetch stations:", err);
        });
    },
    goDetail(station) {
      console.log("Station clicked:", station);
      this.$router.push(`/station/${station.stationReference}`);
    },
    onGroupByChange(value) {
      console.log("Grouping by:", value);
    }
  }
};
</script>


