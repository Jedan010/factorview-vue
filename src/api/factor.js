import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://192.169.88.209:5000'

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

export const getFactorStatsGroup = async (params) => {
  const response = await axios.get(`${API_BASE_URL}/api/factor/stats/group`, { params })
  return response.data
}

export const getFactorStatsIC = async (params) => {
  const response = await axios.get(`${API_BASE_URL}/api/factor/stats/ic`, { params })
  return response.data
}

export const getFactorPerf = async (factorName, params) => {
  const response = await axios.get(`${API_BASE_URL}/api/factor/${factorName}`, { params })
  return response.data
}
export const getFactorUpdate = async (params) => {
  const response = await axios.get(`${API_BASE_URL}/api/factor/update`, { params })
  return response.data
}
