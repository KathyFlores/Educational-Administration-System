var DataModelFactory = (
    function () {
        function _init() {

        }
        _init.prototype = {
            constructor: _init,
            createView: function(data) {
                // ask for implementaion for createView(data)
                console.log("Error: createView is not implemented.");
            }
        };
        return _init;
    }
)();

