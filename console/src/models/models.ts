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

  constructor(public channelRegExpsMember: string[], public channelRegExpsNoMember: string[], public ignoreChannels: ChannelID[], public ignoreUsers: UserID[], ) { }

  static fromJson(json: any) {
    return new UserConfig(json['channel_regexps_member'], json['channel_regexps_nomember'], json['ignore_channels'], json['ignore_users'])
  }

  public toJson(): Object {
    return {
      'channel_regexps_member': this.channelRegExpsMember,
      'channel_regexps_nomember': this.channelRegExpsNoMember,
      'ignore_channels': this.ignoreChannels,
      'ignore_users': this.ignoreUsers,
    }
  }
}
