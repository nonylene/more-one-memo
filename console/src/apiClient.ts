import { Channel, User } from './models/models'

export async function getSlackChannels(): Promise<Channel[]> {
  const response = await fetch('/slack/channels')
  const json: any[] = await response.json()
  return json.map(Channel.fromJson)
}

export async function getSlackUsers(): Promise<User[]> {
  const response = await fetch('/slack/users')
  const json: any[] = await response.json()
  return json.map(User.fromJson)
}
