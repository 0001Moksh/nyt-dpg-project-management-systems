import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle responses
apiClient.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
      window.location.href = '/auth/login';
    }
    return Promise.reject(error.response?.data || error.message);
  }
);

export const authAPI = {
  login: (email: string) => apiClient.post('/api/auth/login', { email }),
  adminLogin: (email: string, password: string) =>
    apiClient.post('/api/auth/admin-login', { email, password }),
  verifyOtp: (email: string, otp: string) =>
    apiClient.post('/api/auth/verify-otp', { email, otp }),
  verifyToken: (token: string) =>
    apiClient.post('/api/auth/verify-token', { token }),
};

export const projectAPI = {
  list: () => apiClient.get('/api/projects'),
  get: (id: number) => apiClient.get(`/api/projects/${id}`),
  create: (data: any) => apiClient.post('/api/projects', data),
  enroll: (projectId: number, token: string) =>
    apiClient.post(`/api/projects/${projectId}/enroll`, { token }),
  getLeaderboard: (projectId: number) =>
    apiClient.get(`/api/projects/${projectId}/leaderboard`),
};

export const teamAPI = {
  create: (data: any) => apiClient.post('/api/teams', data),
  get: (id: number) => apiClient.get(`/api/teams/${id}`),
  invite: (teamId: number, inviteeEmail: string) =>
    apiClient.post(`/api/teams/${teamId}/invite`, { invitee_email: inviteeEmail }),
  respondToInvite: (teamId: number, invitationId: number, approve: boolean) =>
    apiClient.post(`/api/teams/${teamId}/invitations/${invitationId}/respond`, { approve }),
  lock: (teamId: number) => apiClient.post(`/api/teams/${teamId}/lock`, {}),
  getMembers: (teamId: number) => apiClient.get(`/api/teams/${teamId}/members`),
};

export const submissionAPI = {
  upload: (teamId: number, stage: string, fileUrl: string) =>
    apiClient.post(`/api/submissions/${teamId}/${stage}`, { file_url: fileUrl }),
  get: (id: number) => apiClient.get(`/api/submissions/${id}`),
  approve: (submissionId: number, approve: boolean) =>
    apiClient.post(`/api/submissions/${submissionId}/approve`, { approve }),
  getTeamSubmissions: (teamId: number) =>
    apiClient.get(`/api/submissions/team/${teamId}`),
  getFeedback: (submissionId: number) =>
    apiClient.get(`/api/submissions/${submissionId}/feedback`),
};

export const supervisorAPI = {
  getPendingSubmissions: () => apiClient.get('/api/supervisor/submissions'),
  getSubmissionDetail: (submissionId: number) =>
    apiClient.get(`/api/supervisor/submissions/${submissionId}`),
  scoreSubmission: (submissionId: number, score: number, comments?: string) =>
    apiClient.post(`/api/supervisor/submissions/${submissionId}/score`, { score, comments }),
  getStats: () => apiClient.get('/api/supervisor/stats'),
};

export const adminAPI = {
  getRequests: () => apiClient.get('/api/admin/requests'),
  approveRequest: (requestId: number) =>
    apiClient.post(`/api/admin/requests/${requestId}/approve`, {}),
  rejectRequest: (requestId: number) =>
    apiClient.post(`/api/admin/requests/${requestId}/reject`, {}),
  getLogs: (skip?: number, limit?: number) =>
    apiClient.get('/api/admin/logs', { params: { skip, limit } }),
  getStats: () => apiClient.get('/api/admin/stats'),
};

export const chatbotAPI = {
  ask: (question: string) => apiClient.post('/api/chatbot/ask', { question }),
  getChatHistory: (limit?: number) =>
    apiClient.get('/api/chatbot/sessions', { params: { limit } }),
  deleteSession: (sessionId: number) =>
    apiClient.delete(`/api/chatbot/sessions/${sessionId}`),
};

export default apiClient;
