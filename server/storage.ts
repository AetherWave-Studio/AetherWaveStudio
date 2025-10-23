import { type User, type InsertUser, type UpsertUser } from "@shared/schema";
import { randomUUID } from "crypto";

// modify the interface with any CRUD methods
// you might need

export interface IStorage {
  getUser(id: string): Promise<User | undefined>;
  getUserByUsername(username: string): Promise<User | undefined>;
  getUserByEmail(email: string): Promise<User | undefined>;
  createUser(user: InsertUser): Promise<User>;
  upsertUser(user: UpsertUser): Promise<User>;
  updateUserVocalPreference(userId: string, preference: string): Promise<User | undefined>;
  updateUserCredits(userId: string, credits: number, lastReset?: Date): Promise<User | undefined>;
}

export class MemStorage implements IStorage {
  private users: Map<string, User>;

  constructor() {
    this.users = new Map();
  }

  async getUser(id: string): Promise<User | undefined> {
    return this.users.get(id);
  }

  async getUserByUsername(username: string): Promise<User | undefined> {
    return Array.from(this.users.values()).find(
      (user) => user.username === username,
    );
  }

  async getUserByEmail(email: string): Promise<User | undefined> {
    return Array.from(this.users.values()).find(
      (user) => user.email === email,
    );
  }

  async updateUserVocalPreference(userId: string, preference: string): Promise<User | undefined> {
    const user = this.users.get(userId);
    if (user) {
      user.vocalGenderPreference = preference;
      this.users.set(userId, user);
    }
    return user;
  }

  async updateUserCredits(userId: string, credits: number, lastReset?: Date): Promise<User | undefined> {
    const user = this.users.get(userId);
    if (user) {
      user.credits = credits;
      if (lastReset) {
        user.lastCreditReset = lastReset;
      }
      user.updatedAt = new Date();
      this.users.set(userId, user);
    }
    return user;
  }

  async createUser(insertUser: InsertUser): Promise<User> {
    const id = randomUUID();
    const now = new Date();
    const user: User = { 
      id,
      email: insertUser.email ?? null,
      firstName: insertUser.firstName ?? null,
      lastName: insertUser.lastName ?? null,
      profileImageUrl: insertUser.profileImageUrl ?? null,
      username: insertUser.username ?? null,
      vocalGenderPreference: insertUser.vocalGenderPreference ?? 'm',
      credits: 50,
      planType: 'free',
      lastCreditReset: now,
      stripeCustomerId: null,
      stripeSubscriptionId: null,
      createdAt: now,
      updatedAt: now
    };
    this.users.set(id, user);
    return user;
  }

  async upsertUser(userData: UpsertUser): Promise<User> {
    const existingUser = this.users.get(userData.id as string);
    const now = new Date();
    
    if (existingUser) {
      const updatedUser: User = {
        ...existingUser,
        ...userData,
        updatedAt: now
      };
      this.users.set(updatedUser.id, updatedUser);
      return updatedUser;
    } else {
      const newUser: User = {
        ...userData,
        id: userData.id || randomUUID(),
        vocalGenderPreference: userData.vocalGenderPreference || 'm',
        credits: userData.credits ?? 50,
        planType: userData.planType || 'free',
        lastCreditReset: userData.lastCreditReset || now,
        stripeCustomerId: userData.stripeCustomerId || null,
        stripeSubscriptionId: userData.stripeSubscriptionId || null,
        createdAt: now,
        updatedAt: now
      } as User;
      this.users.set(newUser.id, newUser);
      return newUser;
    }
  }
}

export const storage = new MemStorage();
