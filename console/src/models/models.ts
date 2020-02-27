export interface Channel {
  id: string,
  name: string,
}

export interface User {
  id: string,
  name: string,
}

export interface UserConfig {
  channelRegExps: string[],
  ignoreChannels: string[],
  ignoreUsers: string[],
}
