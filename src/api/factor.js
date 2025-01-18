import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:5000'

export const getFactorInfo = async (params) => {
  const response = await axios.get(`${API_BASE_URL}/api/factor`, { params })
  return response.data
}

export const getFactorStats = async (params) => {
  const response = await axios.get(`${API_BASE_URL}/api/factor/stats`, { params })
  return response.data
}

export const getFactorStatsBacktest = async (params) => {
  const response = await axios.get(`${API_BASE_URL}/api/factor/stats/backtest`, { params })
  return response.data
}

export const getFactorPerf = async (factorName, params) => {
  const response = await axios.get(`${API_BASE_URL}/api/factor/${factorName}`, { params })
  return response.data
}
