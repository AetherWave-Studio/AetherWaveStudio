import { sql } from "drizzle-orm";
import { pgTable, text, varchar, timestamp, jsonb, integer, index } from "drizzle-orm/pg-core";
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod";

// Session storage table for Replit Auth (required)
export const sessions = pgTable(
  "sessions",
  {
    sid: varchar("sid").primaryKey(),
    sess: jsonb("sess").notNull(),
    expire: timestamp("expire").notNull(),
  },
  (table) => [index("IDX_session_expire").on(table.expire)],
);

// User storage table
export const users = pgTable("users", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  email: varchar("email").unique(),
  firstName: varchar("first_name"),
  lastName: varchar("last_name"),
  profileImageUrl: varchar("profile_image_url"),
  username: varchar("username").unique(),
  vocalGenderPreference: varchar("vocal_gender_preference").default('m'),
  credits: integer("credits").default(50).notNull(),
  planType: varchar("plan_type").default('free').notNull(), // 'free', 'studio', 'creator', 'all_access'
  lastCreditReset: timestamp("last_credit_reset").defaultNow().notNull(),
  stripeCustomerId: varchar("stripe_customer_id"),
  stripeSubscriptionId: varchar("stripe_subscription_id"),
  createdAt: timestamp("created_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at").defaultNow().notNull(),
});

export const insertUserSchema = createInsertSchema(users).omit({
  id: true,
  createdAt: true,
  updatedAt: true,
});

export type UpsertUser = typeof users.$inferInsert;
export type InsertUser = z.infer<typeof insertUserSchema>;
export type User = typeof users.$inferSelect;

// Uploaded audio files table
export const uploadedAudio = pgTable("uploaded_audio", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  fileName: varchar("file_name").notNull(),
  mimeType: varchar("mime_type").notNull(),
  fileSize: varchar("file_size").notNull(),
  audioData: text("audio_data").notNull(), // Base64 encoded audio data
  userId: varchar("user_id"),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

export const insertUploadedAudioSchema = createInsertSchema(uploadedAudio).omit({
  id: true,
  createdAt: true,
});

export type InsertUploadedAudio = z.infer<typeof insertUploadedAudioSchema>;
export type UploadedAudio = typeof uploadedAudio.$inferSelect;
