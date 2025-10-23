import { 
  type User, 
  type InsertUser, 
  type UpsertUser,
  type ServiceType,
  type CreditCheckResult,
  type CreditDeductionResult,
  SERVICE_CREDIT_COSTS,
  UNLIMITED_SERVICE_PLANS,
} from "@shared/schema";
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
  
  // Centralized credit management
  checkCredits(userId: string, serviceType: ServiceType): Promise<CreditCheckResult>;
  deductCredits(userId: string, serviceType: ServiceType): Promise<CreditDeductionResult>;
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

  async checkCredits(userId: string, serviceType: ServiceType): Promise<CreditCheckResult> {
    const user = this.users.get(userId);
    
    if (!user) {
      return {
        allowed: false,
        reason: 'insufficient_credits',
        currentCredits: 0,
        requiredCredits: SERVICE_CREDIT_COSTS[serviceType],
      };
    }

    const requiredCredits = SERVICE_CREDIT_COSTS[serviceType];
    const hasUnlimitedAccess = UNLIMITED_SERVICE_PLANS[serviceType].includes(user.planType as any);

    if (hasUnlimitedAccess) {
      return {
        allowed: true,
        reason: 'unlimited',
        currentCredits: user.credits,
        requiredCredits: 0,
        planType: user.planType as any,
      };
    }

    const hasSufficientCredits = user.credits >= requiredCredits;
    
    return {
      allowed: hasSufficientCredits,
      reason: hasSufficientCredits ? 'success' : 'insufficient_credits',
      currentCredits: user.credits,
      requiredCredits,
      planType: user.planType as any,
    };
  }

  async deductCredits(userId: string, serviceType: ServiceType): Promise<CreditDeductionResult> {
    const user = this.users.get(userId);
    
    if (!user) {
      return {
        success: false,
        newBalance: 0,
        amountDeducted: 0,
        wasUnlimited: false,
        error: 'User not found',
      };
    }

    const requiredCredits = SERVICE_CREDIT_COSTS[serviceType];
    const hasUnlimitedAccess = UNLIMITED_SERVICE_PLANS[serviceType].includes(user.planType as any);

    if (hasUnlimitedAccess) {
      return {
        success: true,
        newBalance: user.credits,
        amountDeducted: 0,
        wasUnlimited: true,
      };
    }

    if (user.credits < requiredCredits) {
      return {
        success: false,
        newBalance: user.credits,
        amountDeducted: 0,
        wasUnlimited: false,
        error: `Insufficient credits. Required: ${requiredCredits}, Available: ${user.credits}`,
      };
    }

    const newCredits = Math.max(0, user.credits - requiredCredits);
    user.credits = newCredits;
    user.updatedAt = new Date();
    this.users.set(userId, user);

    return {
      success: true,
      newBalance: newCredits,
      amountDeducted: requiredCredits,
      wasUnlimited: false,
    };
  }
}

export const storage = new MemStorage();
