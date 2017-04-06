document.getElementById("navMenu").innerHTML =
'<nav id="navbarsweg">' +
  '<nav class="navbar navbar-default">' +
    '<div class="container-fluid">' +
      '<!-- Brand and toggle get grouped for better mobile display -->' +
      '<div class="navbar-header">' +
        '<button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1" aria-expanded="false">' +
          '<span class="sr-only">Toggle navigation</span>' +
          '<span class="icon-bar"></span>' +
          '<span class="icon-bar"></span>' +
          '<span class="icon-bar"></span>' +
        '</button>' +
        '<a class="navbar-brand" href="/">YouTubeSWEg</a>' +
      '</div>' +

      '<!-- Collect the nav links, forms, and other content for toggling -->' +
      '<div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">' +
        '<ul class="nav navbar-nav navbar-left">' +
          '<li class=active" id="Videos"><a href="/video">Videos</a></li>' +
          '<li id="Channels"><a href="/channel">Channels</a></li>' +
          '<li id="Categories"><a href="/category">Categories</a></li>' +
          '<li id="Playlists"><a href="/playlist">Playlists</a></li>' +
          

        '</ul>' +
        '<ul class="nav navbar-nav navbar-right">' +
        '<li id="About"><a href="/about">About</a></li>' +
        '</ul>' +
      '</div><!-- /.navbar-collapse -->' +
    '</div><!-- /.container-fluid -->' +
  '</nav>' +
'</nav>';

// class Model extends React.Component {
//   constructor() {
//     super();
//     this.state = {
//       title:null,

//     };
//   }
//   render() {
//     return (
//       <button className="square" onClick={() => this.props.onClick()}>
//         {this.state.value}
//       </button>
//     );
//   }
// }


// class Model() extends React.Component {
//   constructor() {
//     super();
//     var model_dict = require('model.json')[this.props.title]
//     this.state = {
//       title:null,

//     };

//   render() {
//     return (
//         <sort_tabs value=this.props.title />
//         <filter_tabs value=this.props.title />
//         <panels value=this.props.data title=this.props.title />
//     );
//   }

// }

// var createModel(data, title) {
//   ReactDOM.render(
//       <Model value=data title=title />,
//       document.getElementById('modelContainer')
//   );
// }

// class Square extends React.Component {
//   render() {
//     return (
//       <button className="square">
//         {/* TODO */}
//       </button>
//     );
//   }
// }

// class Board extends React.Component {
//   renderSquare(i) {
//     return <Square />;
//   }
//   render() {
//     const status = 'Next player: X';
//     return (
//       <div>
//         <div className="status">{status}</div>
//         <div className="board-row">
//           {this.renderSquare(0)}
//           {this.renderSquare(1)}
//           {this.renderSquare(2)}
//         </div>
//         <div className="board-row">
//           {this.renderSquare(3)}
//           {this.renderSquare(4)}
//           {this.renderSquare(5)}
//         </div>
//         <div className="board-row">
//           {this.renderSquare(6)}
//           {this.renderSquare(7)}
//           {this.renderSquare(8)}
//         </div>
//       </div>
//     );
//   }
// }

// class Game extends React.Component {
//   render() {
//     return (
//       <div className="game">
//         <div className="game-board">
//           <Board />
//         </div>
//         <div className="game-info">
//           <div>{/* status */}</div>
//           <ol>{/* TODO */}</ol>
//         </div>
//       </div>
//     );
//   }
// }

// // ========================================
// var createModel() {
//   ReactDOM.render(
//     <Game />,
//     document.getElementById('modelContainer')
//   );
// }
