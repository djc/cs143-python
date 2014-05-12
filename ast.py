import sys

class Node(object):
	
	def __repr__(self):
		n = self.__class__.__name__
		fields = ['%s=%r' % (f, self.__dict__[f]) for f in self.fields]
		return '<%s(%s)>' % (n, ', '.join(fields))
	
	def add(self, ls, level, s):
		ls.append(' ' * (level * 2) + s)
	
	def dump(self, ls, level=0):
		
		self.add(ls, level, '#1')
		self.add(ls, level, RTYPES[self.__class__])
		level += 1
		
		for fn in self.fields:
			
			f = getattr(self, fn)
			if isinstance(f, list):
				if self.__class__ not in IMPLICIT: self.add(ls, level, '(')
				for x in f:
					x.dump(ls, level)
				if self.__class__ not in IMPLICIT: self.add(ls, level, ')')
			elif isinstance(f, Node):
				f.dump(ls, level)
			elif fn == 'type':
				self.add(ls, level - 1, ': ' + f)
			else:
				self.add(ls, level, f)
		
		return ls

class Program(Node):
	fields = 'classes',
	def __init__(self):
		self.classes = []

class Class(Node):
	fields = 'name', 'parent', 'filename', 'features'
	def __init__(self):
		self.name = None
		self.parent = None
		self.filename = None
		self.features = []

class Method(Node):
	fields = 'name', 'formals', 'return_type', 'expr'
	def __init__(self):
		self.name = None
		self.formals = []
		self.return_type = None
		self.expr = None

class Attr(Node):
	fields = 'name', 'type_decl', 'init'
	def __init__(self):
		self.name = None
		self.type_decl = None
		self.init = None

class Formal(Node):
	fields = 'name', 'type_decl'
	def __init__(self):
		self.name = None
		self.type_decl = None

class Branch(Node):
	fields = 'name', 'type_decl', 'expr'
	def __init__(self):
		self.name = None
		self.type_decl = None
		self.expr = None

class Assign(Node):
	fields = 'name', 'expr', 'type'
	def __init__(self):
		self.name = None
		self.expr = None
		self.type = None

class StaticDispatch(Node):
	fields = 'expr', 'type_name', 'name', 'actual', 'type'
	def __init__(self):
		self.expr = None
		self.type_name = None
		self.name = None
		self.actual = []
		self.type = None

class Dispatch(Node):
	fields = 'expr', 'name', 'actual', 'type'
	def __init__(self):
		self.expr = None
		self.name = None
		self.actual = []
		self.type = None

class Cond(Node):
	fields = 'pred', 'then_exp', 'else_exp', 'type'
	def __init__(self):
		self.pred = None
		self.then_exp = None
		self.else_exp = None
		self.type = None

class Loop(Node):
	fields = 'pred', 'body', 'type'
	def __init__(self):
		self.pred = None
		self.body = None
		self.type = None

class TypCase(Node):
	fields = 'expr', 'cases', 'type'
	def __init__(self):
		self.expr = None
		self.cases = []
		self.type = None

class Block(Node):
	fields = 'body', 'type'
	def __init__(self):
		self.body = []
		self.type = None

class Let(Node):
	fields = 'identifier', 'type_decl', 'init', 'body', 'type'
	def __init__(self):
		self.identifier = None
		self.type_decl = None
		self.init = None
		self.body = None
		self.type = None

class Plus(Node):
	fields = 'e1', 'e2', 'type'
	def __init__(self):
		self.e1 = None
		self.e2 = None
		self.type = None

class Sub(Node):
	fields = 'e1', 'e2', 'type'
	def __init__(self):
		self.e1 = None
		self.e2 = None
		self.type = None

class Mul(Node):
	fields = 'e1', 'e2', 'type'
	def __init__(self):
		self.e1 = None
		self.e2 = None
		self.type = None

class Divide(Node):
	fields = 'e1', 'e2', 'type'
	def __init__(self):
		self.e1 = None
		self.e2 = None
		self.type = None

class Neg(Node):
	fields = 'e1', 'type'
	def __init__(self):
		self.e1 = None
		self.type = None

class LT(Node):
	fields = 'e1', 'e2', 'type'
	def __init__(self):
		self.e1 = None
		self.e2 = None
		self.type = None

class EQ(Node):
	fields = 'e1', 'e2', 'type'
	def __init__(self):
		self.e1 = None
		self.e2 = None
		self.type = None

class LEQ(Node):
	fields = 'e1', 'e2', 'type'
	def __init__(self):
		self.e1 = None
		self.e2 = None
		self.type = None

class Comp(Node):
	fields = 'e1', 'type'
	def __init__(self):
		self.e1 = None
		self.type = None

class IntConst(Node):
	fields = 'token', 'type'
	def __init__(self):
		self.token = None
		self.type = None

class BoolConst(Node):
	fields = 'val', 'type'
	def __init__(self):
		self.val = None
		self.type = None

class StringConst(Node):
	fields = 'token', 'type'
	def __init__(self):
		self.token = None
		self.type = None

class New(Node):
	fields = 'type_name', 'type'
	def __init__(self):
		self.type_name = None
		self.type = None

class IsVoid(Node):
	fields = 'e1', 'type'
	def __init__(self):
		self.e1 = None
		self.type = None

class NoExpr(Node):
	fields = 'type',
	def __init__(self):
		self.type = None

class Object(Node):
	fields = 'name', 'type'
	def __init__(self):
		self.name = None
		self.type = None

TYPES = {
	'_program': Program,
	'_class': Class,
	'_method': Method,
	'_dispatch': Dispatch,
	'_object': Object,
	'_string': StringConst,
	'_block': Block,
	'_int': IntConst,
	'_isvoid': IsVoid,
	'_attr': Attr,
	'_new': New,
	'_no_expr': NoExpr,
	'_formal': Formal,
	'_assign': Assign,
	'_bool': BoolConst,
	'_cond': Cond,
	'_eq': EQ,
	'_sub': Sub,
	'_neg': Neg,
	'_let': Let,
	'_loop': Loop,
	'_typcase': TypCase,
	'_branch': Branch,
	'_plus': Plus,
	'_static_dispatch': StaticDispatch,
	'_lt': LT,
	'_mul': Mul,
	'_divide': Divide,
	'_leq': LEQ,
	'_comp': Comp,
}

RTYPES = dict((v, k) for (k, v) in TYPES.iteritems())
IMPLICIT = set((Program, Block, Method, TypCase))

class Pass(object):
	
	def __init__(self, root):
		self.root = root
		self.stack = []
		self.left = [(0, root)]
		self.errors = []
	
	def error(self, msg):
		self.errors.append('%s:1: %s' % (self.stack[1].filename[1:-1], msg))
	
	def visit(self, node, post=None):
		ntype = node.__class__.__name__
		if hasattr(self, ntype) and post is not None:
			getattr(self, ntype)(node, post)
		elif hasattr(self, ntype):
			getattr(self, ntype)(node)
		else:
			print 'no handler for %s' % ntype
	
	def walk(self):
		while self.left:
			
			level, node = self.left.pop(0)
			while self.stack and len(self.stack) > level:
				self.visit(self.stack[-1], 1)
				self.stack.pop()
				
			self.stack.append(node)
			self.visit(node, 0)
			for fn in node.fields:
				f = getattr(node, fn)
				if isinstance(f, Node):
					self.left.insert(0, (level + 1, f))
				elif isinstance(f, list):
					children = [(level + 1, c) for c in f]
					self.left = children + self.left
		
		while self.stack:
			self.visit(self.stack[-1], 1)
			self.stack.pop()
		
		return self.errors

def parse(x):
	
	if isinstance(x, str):
		src = x
	if isinstance(x, file):
		src = x.read()
	
	stack = []
	root = None
	start = False
	node = None
	indent = 0
	
	for ln in src.splitlines():
		
		delta = len(ln) - len(ln.lstrip()) - indent
		assert not delta % 2
		delta /= 2
		
		if delta < 0 and ln.lstrip()[:2] != ': ':
			for i in range(abs(delta)):
				stack.pop()
		
		indent = len(ln) - len(ln.lstrip())
		ln = ln.strip()
		
		if ln.startswith('#'):
			start = True
			continue
		
		if start and ln.startswith('_'):
			stack.append([TYPES[ln](), 0])
			if root is None:
				root = stack[-1][0]
			else:
				prev = stack[-2]
				fname = prev[0].fields[prev[1]]
				field = getattr(prev[0], fname)
				if isinstance(field, list):
					field.append(stack[-1][0])
				else:
					prev[1] += 1
					setattr(prev[0], fname, stack[-1][0])
				
			continue
		
		if ln == '(' or ln == ')':
			continue
		
		if ln[0:2] == ': ':
			
			while delta < -1:
				stack.pop()
				delta += 1
			
			top = stack[-1]
			assert 'type' in top[0].fields, top[0]
			top[0].type = ln[2:]
			top[1] += 1
			stack.pop()
			continue
		
		top = stack[-1]
		field = top[0].fields[top[1]]
		if field == 'formals':
			top[1] += 1
			field = top[0].fields[top[1]]
			
		setattr(top[0], field, ln)
		top[1] += 1
	
	return root

def dump(root):
	return '\n'.join(root.dump([]))

if __name__ == '__main__':
	print dump(parse(open(sys.argv[1])))
