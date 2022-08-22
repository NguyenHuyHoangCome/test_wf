module.exports = (on, config) => {
    on('before:browser:launch', (browser = {}, options) => {
            options.args.push('--windows-size=1280,720');
            return options;
    });
};
