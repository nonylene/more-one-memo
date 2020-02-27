import React, { useState, useEffect } from 'react';
import Autocomplete from '@material-ui/lab/Autocomplete';
import TextField from '@material-ui/core/TextField';

import { Channel } from '../../models/models';

const channelToLabel = (channel: Channel) => `${channel.name} | ${channel.id}`

export default function IgnoreChannelsInput() {

  const [channels, setChannels] = useState<Channel[]>([]);

  useEffect(() => {
    document.title = `You clicked ${count} times`;
  }, []);

  return (
    <div className="IgnoreChannelsInput">
      <Autocomplete
        multiple
        options={exampleChannels}
        getOptionLabel={channelToLabel}
        value={channels}
        onChange={(_, values) => setChannels(values)}
        renderInput={params => (
          <TextField
            {...params}
            label="Ignore channels"
            placeholder="Channels"
            fullWidth
          />
        )}
      />
    </div>
  );
}

const exampleChannels: Channel[] = [
  { id: "C1111", name: "#foobar" },
  { id: "C1122", name: "#foobaz" },
  { id: "C1145", name: "#あああ" },
]
