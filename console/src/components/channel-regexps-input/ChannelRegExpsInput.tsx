import React, { useState } from 'react';
import Autocomplete from '@material-ui/lab/Autocomplete';
import TextField from '@material-ui/core/TextField';

export default function ChannelRegExpsInput() {

  const [channelRegExps, setChannelRegExps] = useState<string[]>([]);

  return (
    <div className="ChannelRegExpsInput">
      <Autocomplete<string>
        multiple
        freeSolo={true}
        value={channelRegExps}
        onChange={(_, values) => setChannelRegExps(values)}
        renderInput={params => (
          <TextField
            {...params}
            fullWidth
            label="Channel RegExps"
            placeholder="RegExp"
          />
        )}
      />
    </div>
  );
}
