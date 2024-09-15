<template>
  <div>
    <h1>Log Report</h1>

    <!-- Main table showing server entries -->
    <table>
      <thead>
        <tr>
          <th>Server</th>
          <th>Sender</th>
          <th>Entries</th>
        </tr>
      </thead>
      <tbody>
          <template v-for="(data, server) in allLogs" :key="server">
            <tr v-for="(logs, sender, senderIndex) in data.logs" :key="sender">
              <td v-if="senderIndex === 0" :rowspan="Object.keys(data.logs).length">{{ server }}</td>
              <td>{{ sender }}</td>
              <td>{{ data.counts[sender] }}</td>
            </tr>
          </template>
      </tbody>


    </table>

    <!-- Detailed file information -->
    <div v-for="(data, server) in allLogs" :key="server" class="server-section">
      <div class="server-name">Details for Server: {{ server }}</div>
      <div v-for="(logs, sender) in data.logs" :key="sender" class="file-details">
        <strong>Sender: {{ sender }}</strong>
        <ul>
          <li v-for="log in logs" :key="log.filename">
            <strong>File:</strong> {{ log.filename }} <br>
            <strong>Date:</strong> {{ log.date }} <br>
            <strong>Time:</strong> {{ log.time }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      allLogs: {}
    };
  },
  created() {
    this.fetchLogs();
  },
  methods: {
    fetchLogs() {
      fetch('http://127.0.0.1:5000/logs') // Replace with your Flask server URL
        .then(response => response.json())
        .then(data => {
          this.allLogs = data;
        })
        .catch(error => {
          console.error('Error fetching logs:', error);
        });
    }
  }
};
</script>

<style scoped>
body {
  font-family: Arial, sans-serif;
  margin: 20px;
}
h1 {
  font-size: 24px;
}
table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}
table, th, td {
  border: 1px solid black;
}
th, td {
  padding: 10px;
  text-align: left;
}
th {
  background-color: #f2f2f2;
}
.server-section {
  margin-top: 30px;
}
.server-name {
  font-size: 20px;
  margin-bottom: 10px;
  font-weight: bold;
}
.file-details {
  margin-left: 20px;
}
</style>
