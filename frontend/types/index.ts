// User Types
export type UserRole = 'STUDENT' | 'SUPERVISOR' | 'ADMIN';

export interface User {
  id: string;
  email: string;
  name: string;
  rollNo?: string;
  branch?: string;
  batch?: string;
  role: UserRole;
  profileImage?: string;
  createdAt: string;
  updatedAt: string;
}

// Authentication Types
export interface AuthResponse {
  token: string;
  refreshToken: string;
  user: User;
}

export interface OTPRequest {
  email: string;
}

export interface OTPVerify {
  email: string;
  otp: string;
}

// Project Types
export type ProjectStage = 'SYNOPSIS' | 'PROGRESS_1' | 'PROGRESS_2' | 'FINAL_SUBMISSION';

export interface Project {
  id: string;
  title: string;
  description: string;
  branch: string;
  batch: string;
  supervisor?: Supervisor;
  createdBy: User;
  createdAt: string;
  updatedAt: string;
  enrollmentStatus: 'OPEN' | 'CLOSED' | 'ARCHIVED';
  enrollmentLink: string;
}

// Team Types
export interface TeamMember {
  id: string;
  user: User;
  role: 'LEADER' | 'MEMBER';
  joinedAt: string;
}

export interface Team {
  id: string;
  name: string;
  project: Project;
  members: TeamMember[];
  status: 'FORMING' | 'ACTIVE' | 'COMPLETED';
  createdAt: string;
}

// Supervisor Types
export interface Supervisor extends User {
  department: string;
  assignedProjects: Project[];
}

// Submission Types
export interface Submission {
  id: string;
  team: Team;
  stage: ProjectStage;
  document: {
    url: string;
    name: string;
    uploadedAt: string;
  };
  teamApprovalStatus: 'PENDING' | 'APPROVED' | 'REJECTED';
  supervisorReview?: {
    status: 'PENDING' | 'APPROVED' | 'REJECTED';
    feedback?: string;
    score?: number;
    reviewedAt: string;
  };
  submittedAt: string;
  updatedAt: string;
}

// Scoring Types
export interface StageScore {
  stage: ProjectStage;
  supervisorScore: number; // out of 10
  submittedAt: string;
}

export interface TeamScore {
  team: Team;
  stageScores: StageScore[];
  supervisorAverage: number;
  adminScore?: number; // out of 20
  finalScore?: number; // out of 30
  rank?: number;
}

// Leaderboard Types
export interface LeaderboardEntry {
  rank: number;
  teamName: string;
  projectTitle: string;
  branch: string;
  supervisor: string;
  supervisorAverage: number;
  adminScore: number;
  finalScore: number;
}

// Notification Types
export type NotificationType = 'EMAIL' | 'IN_APP' | 'BOTH';

export interface Notification {
  id: string;
  recipient: User;
  title: string;
  message: string;
  type: NotificationType;
  read: boolean;
  createdAt: string;
}

// RAG Chatbot Types
export interface ChatMessage {
  id: string;
  sender: 'USER' | 'BOT';
  content: string;
  timestamp: string;
  relevantDocuments?: string[];
}

export interface ChatSession {
  id: string;
  user: User;
  role: UserRole;
  messages: ChatMessage[];
  createdAt: string;
}

// Analytics Types
export interface RiskPrediction {
  projectId: string;
  riskLevel: 'LOW' | 'MEDIUM' | 'HIGH';
  factors: string[];
  predictedDelay?: number; // in days
  recommendations: string[];
}

// API Response Types
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

export interface PaginatedResponse<T> {
  success: boolean;
  data: T[];
  total: number;
  page: number;
  pageSize: number;
  totalPages: number;
}
