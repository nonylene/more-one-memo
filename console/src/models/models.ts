export type ChannelID = string

export class Channel {

  constructor(public id: ChannelID, public name: string) { }

  static fromJson(json: any) {
    return new Channel(json['id'], json['name'])
  }
}

export type UserID = string

export class User {

  constructor(public id: UserID, public name: string) { }

  static fromJson(json: any) {
    return new User(json['id'], json['name'])
  }
}

export class UserConfig {

  constructor(public channelRegExps: string[], public ignoreChannels: ChannelID[], public ignoreUsers: UserID[], ) { }

  static fromJson(json: any) {
    return new UserConfig(json['channel_regexps'], json['ignore_channels'], json['ignore_users'])
  }
}
