#define buffer_size 1000

static int tap_fd;
char *tapaddr;
char tap_buffer[buffer_size];

int tap_alloc(char *dev, int flags);
void tap_init();
int tap_read();
int tap_write(char *buf, int len);