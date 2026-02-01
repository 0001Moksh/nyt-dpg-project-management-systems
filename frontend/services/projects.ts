import { apiClient } from './api';
import { Project, Team, Submission, LeaderboardEntry, PaginatedResponse } from '@/types';

export const projectService = {
  // Projects
  async getAllProjects(page = 1, limit = 10) {
    return apiClient.get<PaginatedResponse<Project>>(`/projects?page=${page}&limit=${limit}`);
  },

  async getProjectById(id: string) {
    return apiClient.get<Project>(`/projects/${id}`);
  },

  async createProject(projectData: any) {
    return apiClient.post<Project>('/projects', projectData);
  },

  async updateProject(id: string, data: any) {
    return apiClient.put<Project>(`/projects/${id}`, data);
  },

  async generateEnrollmentLink(projectId: string) {
    return apiClient.post<{ enrollmentLink: string }>(
      `/projects/${projectId}/generate-enrollment-link`,
      {}
    );
  },

  // Teams
  async getTeamsByProject(projectId: string) {
    return apiClient.get<Team[]>(`/projects/${projectId}/teams`);
  },

  async getTeamById(teamId: string) {
    return apiClient.get<Team>(`/teams/${teamId}`);
  },

  async createTeam(projectId: string, teamData: any) {
    return apiClient.post<Team>(`/projects/${projectId}/teams`, teamData);
  },

  async joinTeam(teamId: string) {
    return apiClient.post<Team>(`/teams/${teamId}/join`, {});
  },

  async leaveTeam(teamId: string) {
    return apiClient.post(`/teams/${teamId}/leave`, {});
  },

  async approveTeamMember(teamId: string, memberId: string) {
    return apiClient.post<Team>(`/teams/${teamId}/members/${memberId}/approve`, {});
  },

  // Submissions
  async getSubmissionsByTeam(teamId: string) {
    return apiClient.get<Submission[]>(`/teams/${teamId}/submissions`);
  },

  async getSubmissionById(submissionId: string) {
    return apiClient.get<Submission>(`/submissions/${submissionId}`);
  },

  async uploadSubmission(teamId: string, stage: string, file: File) {
    return apiClient.uploadFile<Submission>(
      `/teams/${teamId}/submissions`,
      file,
      { stage }
    );
  },

  async approveSubmission(submissionId: string) {
    return apiClient.post<Submission>(`/submissions/${submissionId}/approve`, {});
  },

  async rejectSubmission(submissionId: string, reason: string) {
    return apiClient.post<Submission>(`/submissions/${submissionId}/reject`, { reason });
  },

  // Supervisor Review
  async reviewSubmission(submissionId: string, score: number, feedback: string) {
    return apiClient.post<Submission>(`/submissions/${submissionId}/review`, {
      score,
      feedback,
    });
  },

  // Leaderboard
  async getLeaderboard(projectId?: string) {
    const url = projectId
      ? `/leaderboard?projectId=${projectId}`
      : '/leaderboard';
    return apiClient.get<LeaderboardEntry[]>(url);
  },

  // Admin - Assign Supervisor
  async assignSupervisor(teamId: string, supervisorId: string) {
    return apiClient.post<Team>(`/teams/${teamId}/assign-supervisor`, {
      supervisorId,
    });
  },

  // Get project enrollment stats
  async getProjectStats(projectId: string) {
    return apiClient.get(`/projects/${projectId}/stats`);
  },
};
