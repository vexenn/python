const oracledb = require('oracledb');
require('dotenv').config(); // Fallback loader

try {
  oracledb.initOracleClient();
} catch (err) {
  // Suppress multi-initialization warnings during test loops
}

const dbConfig = {
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  connectString: process.env.DB_CONNECT_STRING
};

// DIAGNOSTIC LOGS: Let the terminal tell you exactly what it reads
// console.log("=== DB ENVIRONMENT CONFIG CHECK ===");
// console.log("Target Username:", dbConfig.user);
// console.log("Target Connection String:", dbConfig.connectString);
// console.log("===================================");

async function runQuery(sql, binds = []) {
  let connection;
  try {
    connection = await oracledb.getConnection(dbConfig);
    const result = await connection.execute(sql, binds, { autoCommit: true });
    return result;
  } catch (error) {
    console.error('Database query execution error:', error);
    throw error;
  } finally {
    if (connection) {
      await connection.close();
    }
  }
}

module.exports = { runQuery };