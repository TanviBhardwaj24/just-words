export interface User {
  id: number;
  name: string;
  age: number;
  location: string;
  interests: string[];
}

export interface Recommendation {
  id: number;
  type: string;
  title: string;
  description: string;
  user_id: number;
}

export interface EmailContent {
  subject: string;
  body: string;
}

export interface AllUsers {
  id: number;
  name: string;
  age: number;
  location: string;
  interests: string[];
  recommendations: Recommendation[];
  facebook?: string;
  instagram?: string;
  linkedin?: string;
  github?: string;
}
