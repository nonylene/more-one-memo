import { Channel, User, UserConfig } from './models/models'

export async function getSlackChannels(): Promise<Channel[]> {
  const response = await fetch('/api/slack/channels')
  const json: any[] = await response.json()
  return json.map(Channel.fromJson)
}

export async function getSlackUsers(): Promise<User[]> {
  const response = await fetch('/api/slack/users')
  const json: any[] = await response.json()
  return json.map(User.fromJson)
}

export async function getUserConfig(): Promise<UserConfig> {
  const response = await fetch('/api/config')
  const json: any[] = await response.json()
  return UserConfig.fromJson(json)
}
