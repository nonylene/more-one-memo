export class Channel {

  constructor(public id: string, public name: string) { }

  static fromJson(json: any) {
    return new Channel(json['id'], json['name'])
  }
}

export class User {

  constructor(public id: string, public name: string) { }

  static fromJson(json: any) {
    return new User(json['id'], json['name'])
  }
}

export class UserConfig {

  constructor(public channelRegExps: string[], public ignoreChannels: string[], public ignoreUsers: string[], ) { }

  static fromJson(json: any) {
    return new UserConfig(json['channel_regexps'], json['ignore_channels'], json['ignore_users'])
  }
}
