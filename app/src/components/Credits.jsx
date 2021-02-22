import React from 'react';

import Box from '@material-ui/core/Box';
import Link from '@material-ui/core/Link';

export default function Credits() {
  return (
    <Box textAlign="center" p={2}>
      <div>
        <Link
          target="_blank"
          rel="noreferrer"
          underline="always"
          href="https://github.com/degorov/smart-lamp"
        >
          Репозиторий проекта на GitHub
        </Link>
      </div>
      <div>
        Application icon made by&nbsp;
        <Link target="_blank" rel="noreferrer" underline="always" href="https://www.freepik.com">
          Freepik
        </Link>
        &nbsp;from&nbsp;
        <Link target="_blank" rel="noreferrer" underline="always" href="https://www.flaticon.com/">
          www.flaticon.com
        </Link>
      </div>
    </Box>
  );
}
